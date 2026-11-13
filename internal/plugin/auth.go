package plugin

import (
	"context"
	"encoding/json"
	"errors"
	"net/http"
	"net/url"
	"strings"

	"github.com/yuluo688/credit-manager/internal/service"
	"github.com/yuluo688/credit-manager/internal/store"
	"github.com/yuluo688/credit-manager/internal/usageparse"

	"github.com/router-for-me/CLIProxyAPI/v8/sdk/pluginapi"
)

func authenticate(raw []byte) ([]byte, error) {
	svc := service.Current()
	if svc == nil {
		return okEnvelope(pluginapi.FrontendAuthResponse{Authenticated: false})
	}
	var req pluginapi.FrontendAuthRequest
	if err := json.Unmarshal(raw, &req); err != nil {
		return okEnvelope(pluginapi.FrontendAuthResponse{Authenticated: false})
	}
	// CLIProxyAPI's management center queries the read-only model directory
	// without a client Key. Keep model execution exclusively Key-authenticated.
	// Globally disabled models are stripped by the response interceptor; per-Key
	// allowlists are also applied there when the request carries a valid key.
	if publicModelDirectoryRequest(req.Method, req.Path) {
		principal, meta, ok := svc.Authenticate(context.Background(), normalizedAuthHeaders(req.Headers, req.Query))
		if !ok {
			return okEnvelope(pluginapi.FrontendAuthResponse{
				Authenticated: true,
				Principal:     "credit-manager:model-directory",
				Metadata:      map[string]string{"plugin": service.PluginID, "public_models": "true"},
			})
		}
		meta["public_models"] = "true"
		return okEnvelope(pluginapi.FrontendAuthResponse{
			Authenticated: true,
			Principal:     principal,
			Metadata:      meta,
		})
	}
	principal, meta, ok := svc.Authenticate(context.Background(), normalizedAuthHeaders(req.Headers, req.Query))
	if !ok {
		return okEnvelope(pluginapi.FrontendAuthResponse{Authenticated: false})
	}
	return okEnvelope(pluginapi.FrontendAuthResponse{
		Authenticated: true,
		Principal:     principal,
		Metadata:      meta,
	})
}

func publicModelDirectoryRequest(method, path string) bool {
	if !strings.EqualFold(strings.TrimSpace(method), http.MethodGet) {
		return false
	}
	switch strings.TrimRight(strings.TrimSpace(path), "/") {
	case "/v1/models", "/v1beta/models":
		return true
	default:
		return false
	}
}

// normalizedAuthHeaders returns a copy of headers where native client
// credentials are rewritten to the canonical Authorization: Bearer form so the
// downstream chain (principal -> userApiKey -> caller_scope) sees a uniform
// credential. Priority: explicit Authorization > x-goog-api-key > x-api-key
// > ?key= query parameter (Gemini SDK style). The original headers are not
// mutated.
func normalizedAuthHeaders(headers http.Header, query url.Values) http.Header {
	if headers != nil && strings.TrimSpace(headers.Get("Authorization")) != "" {
		return headers
	}
	token := ""
	if headers != nil {
		for _, name := range []string{"x-goog-api-key", "x-api-key"} {
			if v := strings.TrimSpace(headers.Get(name)); v != "" {
				token = v
				break
			}
			for k, values := range headers {
				if strings.EqualFold(k, name) {
					for _, v := range values {
						if v = strings.TrimSpace(v); v != "" {
							token = v
						}
					}
				}
				if token != "" {
					break
				}
			}
		}
	}
	if token == "" && len(query) > 0 {
		token = strings.TrimSpace(query.Get("key"))
	}
	if token == "" {
		return headers
	}
	out := headers.Clone()
	if out == nil {
		out = http.Header{}
	}
	out.Set("Authorization", "Bearer "+token)
	return out
}

func interceptRequestAfterAuth(raw []byte) ([]byte, error) {
	svc := service.Current()
	if svc == nil {
		return okEnvelope(pluginapi.RequestInterceptResponse{})
	}
	var req pluginapi.RequestInterceptRequest
	if err := json.Unmarshal(raw, &req); err != nil {
		return nil, err
	}
	requestID := strings.TrimSpace(req.RequestID)
	if requestID == "" {
		return okEnvelope(pluginapi.RequestInterceptResponse{})
	}
	ctx := context.Background()
	key, _, err := svc.ResolveIdentity(ctx, req.Headers, req.Metadata)
	if !isNativeImageProtocol(req.SourceFormat) && !isImageOnlyModel(firstNonEmpty(req.RequestedModel, req.Model)) {
		// CPA invokes this hook before its executor. Carry the lifecycle request ID
		// into our executor, then remove it before the nested host model call.
		if err == nil && req.Stream {
			trackStreamLifecycle(requestID, svc)
			return okEnvelope(pluginapi.RequestInterceptResponse{Headers: http.Header{
				lifecycleRequestHeader: []string{requestID},
			}})
		}
		return okEnvelope(pluginapi.RequestInterceptResponse{})
	}
	if err != nil {
		// No attributable plugin key — cannot write usage_ledger.
		return okEnvelope(quotaRejectResponse(http.StatusUnauthorized, err.Error()))
	}
	modelName := firstNonEmpty(req.RequestedModel, req.Model)
	plan, err := svc.BuildReservePlan(ctx, modelName, req.Body)
	if err != nil {
		if errors.Is(err, store.ErrModelDisabled) {
			recordRejectedAttempt(ctx, svc, key, firstNonEmpty(modelName, "unknown"), "failed", service.SourceAttemptRejected, "model_disabled:"+err.Error())
			return okEnvelope(modelDisabledRejectResponse(err.Error()))
		}
		recordRejectedAttempt(ctx, svc, key, firstNonEmpty(modelName, "unknown"), "failed", service.SourceAttemptRejected, "reserve_rejected:"+err.Error())
		return okEnvelope(quotaRejectResponse(http.StatusPaymentRequired, err.Error()))
	}
	reservation, err := svc.Reserve(ctx, key, plan, "")
	if err != nil {
		if errors.Is(err, store.ErrModelNotAllowed) {
			recordRejectedAttempt(ctx, svc, key, plan.Model, "failed", service.SourceAttemptRejected, "model_not_allowed:"+err.Error())
			return okEnvelope(modelNotAllowedRejectResponse(err.Error()))
		}
		recordRejectedAttempt(ctx, svc, key, plan.Model, "failed", service.SourceAttemptRejected, "limit_rejected:"+err.Error())
		return okEnvelope(quotaRejectResponse(http.StatusTooManyRequests, err.Error()))
	}
	svc.TrackAuthCapture(reservation.ID, plan.Model, req.Model, req.RequestedModel)
	if err := svc.AdmitAuth(ctx, reservation.ID, authIdentityFromIntercept(req)); err != nil {
		settleAttemptOrRelease(ctx, svc, reservation, plan.Model, "failed", service.SourceAttemptFailed, "auth_concurrency:"+err.Error())
		return okEnvelope(quotaRejectResponse(http.StatusTooManyRequests, err.Error()))
	}
	imageHoldsMu.Lock()
	// Image holds have no stream goroutine of their own. If the completion
	// callback never arrives, stop refreshing the heartbeat at the stale
	// timeout so the hold cannot pin the key forever.
	imageHolds[requestID] = imageHold{reservation: reservation, plan: plan, stopHeart: startReservationHeartbeat(svc, reservation.ID, svc.Config().Stream.StaleReservationTimeout)}
	imageHoldsMu.Unlock()
	return okEnvelope(pluginapi.RequestInterceptResponse{})
}

func completeInterceptedRequest(raw []byte) ([]byte, error) {
	svc := service.Current()
	if svc == nil {
		return okEnvelope(map[string]any{})
	}
	var req pluginapi.RequestCompletion
	if err := json.Unmarshal(raw, &req); err != nil {
		return nil, err
	}
	completeStreamLifecycle(req)
	requestID := strings.TrimSpace(req.RequestID)
	imageHoldsMu.Lock()
	hold, ok := imageHolds[requestID]
	if ok {
		delete(imageHolds, requestID)
	}
	imageHoldsMu.Unlock()
	if !ok {
		return okEnvelope(map[string]any{})
	}
	if hold.stopHeart != nil {
		hold.stopHeart()
	}
	ctx := context.Background()
	defer svc.ReleaseIfHeld(ctx, hold.reservation.ID, "unsettled_exit")
	if req.Outcome != pluginapi.RequestCompletionSucceeded {
		result, source := "failed", service.SourceAttemptFailed
		if req.Outcome == pluginapi.RequestCompletionCanceled {
			result, source = "cancelled", service.SourceAttemptCancelled
		}
		settleAttemptOrRelease(ctx, svc, hold.reservation, hold.plan.Model, result, source, "image_"+string(req.Outcome))
		return okEnvelope(map[string]any{})
	}
	metrics := usageMetricsFromRequest(nil, req.StartedAt, req.CompletedAt, resultFromStatus(req.StatusCode))
	if settleErr := svc.SettleFromUsage(ctx, hold.reservation, hold.plan, usageparse.Result{}, firstNonEmpty(req.SourceFormat, "openai-image"), metrics); settleErr != nil {
		_ = svc.Release(ctx, hold.reservation.ID, "settle_failed")
	}
	return okEnvelope(map[string]any{})
}

// interceptModelDirectoryResponse strips models the caller cannot use from
// GET /v1/models and /v1beta/models responses. Globally disabled models are
// always removed; when the request carries a valid plugin key (Bearer,
// x-goog-api-key, x-api-key, or ?key= — all normalized at authenticate time
// into the host's caller_scope metadata), the key's allowed_models allowlist
// further narrows the directory.
func interceptModelDirectoryResponse(raw []byte) ([]byte, error) {
	svc := service.Current()
	if svc == nil {
		return okEnvelope(pluginapi.ResponseInterceptResponse{})
	}
	var req pluginapi.ResponseInterceptRequest
	if err := json.Unmarshal(raw, &req); err != nil {
		return nil, err
	}
	ctx := context.Background()
	key := resolveDirectoryKey(ctx, svc, req)
	filtered, changed, err := svc.FilterModelDirectoryForKey(ctx, req.Body, key)
	if err != nil {
		return nil, err
	}
	if !changed {
		return okEnvelope(pluginapi.ResponseInterceptResponse{})
	}
	return okEnvelope(pluginapi.ResponseInterceptResponse{Body: filtered})
}

// resolveDirectoryKey identifies the requesting plugin key for a model
// directory response. ResolveIdentity first checks credential headers
// (Bearer / x-goog-api-key / x-api-key, which survive into RequestHeaders),
// then the caller_scope metadata the host derived from the authenticated
// principal — which is how ?key= clients are identified. Unresolvable or
// invalid keys yield nil: the directory degrades to global filtering only.
func resolveDirectoryKey(ctx context.Context, svc *service.Service, req pluginapi.ResponseInterceptRequest) *store.PluginKey {
	key, _, err := svc.ResolveIdentity(ctx, req.RequestHeaders, req.Metadata)
	if err == nil && strings.TrimSpace(key.ID) != "" {
		return &key
	}
	return nil
}

func modelNotAllowedRejectResponse(message string) pluginapi.RequestInterceptResponse {
	body, _ := json.Marshal(map[string]any{
		"error": map[string]any{"message": message, "type": "model_not_allowed", "code": "model_not_allowed"},
	})
	return pluginapi.RequestInterceptResponse{
		Terminate:    true,
		StatusCode:   http.StatusForbidden,
		ResponseBody: body,
	}
}

func modelDisabledRejectResponse(message string) pluginapi.RequestInterceptResponse {
	body, _ := json.Marshal(map[string]any{
		"error": map[string]any{"message": message, "type": "model_disabled", "code": "model_disabled"},
	})
	return pluginapi.RequestInterceptResponse{
		Terminate:    true,
		StatusCode:   http.StatusForbidden,
		ResponseBody: body,
	}
}

func authIdentityFromIntercept(req pluginapi.RequestInterceptRequest) store.AuthIdentity {
	meta := req.Metadata
	return store.AuthIdentity{
		AuthID:    firstNonEmpty(metadataString(meta, "selected_auth_id"), metadataString(meta, "auth_id")),
		AuthIndex: firstNonEmpty(metadataString(meta, "selected_auth_index"), metadataString(meta, "auth_index")),
		Provider:  firstNonEmpty(metadataString(meta, "selected_auth_provider"), metadataString(meta, "auth_provider"), metadataString(meta, "provider")),
	}
}

func quotaRejectResponse(status int, message string) pluginapi.RequestInterceptResponse {
	if status <= 0 {
		status = http.StatusForbidden
	}
	body, _ := json.Marshal(map[string]any{
		"error": map[string]any{"message": message, "type": "insufficient_quota", "code": "limit_rejected"},
	})
	return pluginapi.RequestInterceptResponse{
		Terminate:    true,
		StatusCode:   status,
		ResponseBody: body,
	}
}
