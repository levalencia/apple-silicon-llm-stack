# Architecture Decision Records - Go LLM Gateway

## ADR-001: Use Standard Library Only

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need minimal dependencies for:
- Fast builds
- Security surface area
- Simplicity

### Decision

Use Go standard library only (net/http, slog, context).

### Consequences

**Positive**:
- No external dependencies
- Fast compilation
- Easy deployment

**Negative**:
- Missing features from frameworks (routing, validation)
- More code to write

---

## ADR-002: Use slog for Logging

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need structured JSON logging for:
- Production log aggregation
- Easy searching/filtering

### Decision

Use Go's slog package:

```go
slog.SetDefault(slog.New(slog.NewJSONHandler(os.Stdout, nil)))
slog.Info("request", "method", r.Method)
```

### Consequences

**Positive**:
- Structured logging
- JSON output
- Built into standard library

---

## ADR-003: Simple Environment Configuration

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need simple configuration:
- No external config libraries
- Environment variables preferred

### Decision

Use simple environment variable loading:

```go
func getEnv(key, def string) string {
    if v := os.Getenv(key); v != "" {
        return v
    }
    return def
}
```

### Consequences

**Positive**:
- Simple implementation
- No dependencies
- Easy to use

**Negative**:
- No nested config
- No file-based config

---

## ADR-004: Generic Response Type

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need type-safe API responses:
- Consistent error handling
- Type safety

### Decision

Use Go generics:

```go
type Response[T any] struct {
    Success bool   `json:"success"`
    Data    T      `json:"data,omitempty"`
    Error   string `json:"error,omitempty"`
}
```

### Consequences

**Positive**:
- Type-safe
- Consistent API
- Works with any type

---

## ADR-005: Middleware Chain Pattern

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need composable HTTP processing:
- Request ID
- Logging
- CORS
- Rate limiting

### Decision

Implement chain of responsibility:

```go
func Chain(h http.Handler, middleware ...func(http.Handler) http.Handler) http.Handler {
    for _, m := range middleware {
        h = m(h)
    }
    return h
}
```

### Consequences

**Positive**:
- Composable
- Easy to add middleware
- Clear order

---

## ADR-006: CGO for Metal Integration

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need direct Metal engine access:
- Performance
- Low latency
- Feature parity

### Decision

Use CGO:

```go
// #include "metal_inference/engine.h"
import "C"
```

### Consequences

**Positive**:
- Direct access
- Performance
- Full features

**Negative**:
- Platform specific
- Build complexity

---

## ADR-007: Graceful Shutdown

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need clean server shutdown:
- Drain active requests
- Clean resource release

### Decision

Use context for shutdown:

```go
srv := &http.Server{...}
go srv.ListenAndServe()

quit := make(chan os.Signal, 1)
signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
<-quit

srv.Shutdown(context.Background())
```

### Consequences

**Positive**:
- No dropped requests
- Clean shutdown
- Proper cleanup
