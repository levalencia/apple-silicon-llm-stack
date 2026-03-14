# Go LLM Gateway - Design Patterns & SOLID Principles

## Design Patterns

### 1. Middleware Pattern

Chain of responsibility for HTTP middleware:

```go
func Chain(h http.Handler, middleware ...func(http.Handler) http.Handler) http.Handler {
    for _, m := range middleware {
        h = m(h)
    }
    return h
}

// Middleware signature
func Logger(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        slog.Info("request", "method", r.Method, "url", r.URL.Path)
        next.ServeHTTP(w, r)
    })
}
```

**Usage**:
```go
handler := Chain(router,
    RequestID,
    Logger,
    Recover,
    CORS,
    RateLimit,
)
```

### 2. Handler Functions

HTTP handlers as functions:

```go
func Chat(engine *Engine) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        // Handle chat
    }
}
```

### 3. Generic Response Type

Type-safe API responses:

```go
type Response[T any] struct {
    Success bool   `json:"success"`
    Data    T      `json:"data,omitempty"`
    Error   string `json:"error,omitempty"`
}

// Usage
Response[string]{Success: true, Data: "hello"}
Response[struct{}]{Success: false, Error: "not found"}
```

### 4. Domain Errors

Custom error types:

```go
type DomainError struct {
    Code    string
    Message string
    Err     error
}

func (e *DomainError) Error() string {
    return e.Message
}

func (e *DomainError) Unwrap() error {
    return e.Err
}

func NewDomainError(code, message string, err error) *DomainError {
    return &DomainError{Code: code, Message: message, Err: err}
}
```

### 5. CGO Bridge

Go to C++ interop:

```go
// #include <stdlib.h>
import "C"
import "unsafe"

type Engine struct {
    ptr *C.struct_MTLEngine
}

func NewEngine() *Engine {
    return &Engine{
        ptr: C.mtle_engine_create(nil),
    }
}

func (e *Engine) Destroy() {
    if e.ptr != nil {
        C.mtle_engine_destroy(e.ptr)
    }
}
```

## SOLID Principles

### Single Responsibility

| File | Responsibility |
|------|----------------|
| `config/config.go` | Configuration loading |
| `model/model.go` | Domain types |
| `handlers/handlers.go` | HTTP request handling |
| `middleware/middleware.go` | HTTP middleware |
| `cgobridge/bridge.go` | CGO interop |

### Open/Closed

Extending without modification:

```go
// Add new error types without changing existing code
var (
    ErrInvalidArgument = errors.New("invalid argument")
    ErrOutOfMemory     = errors.New("out of memory")
    // Add more as needed
)
```

### Liskov Substitution

```go
// Any http.Handler works
func applyMiddleware(h http.Handler) http.Handler {
    return Logger(h) // Works with any handler
}
```

### Interface Segregation

```go
// Small interfaces
type Engine interface {
    Infer(prompt string) string
    Destroy()
}
```

### Dependency Inversion

```go
// Handler depends on interface, not concrete
func NewChatHandler(engine Engine) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        engine.Infer(prompt)
    }
}
```

## Error Handling Patterns

### Error Wrapping

```go
func process() error {
    if err := loadModel(); err != nil {
        return fmt.Errorf("failed to load model: %w", err)
    }
    return nil
}
```

### Error Types

```go
func handleError(w http.ResponseWriter, r *http.Request) {
    err := doSomething()
    if errors.Is(err, ErrInvalidArgument) {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    if errors.Is(err, ErrOutOfMemory) {
        http.Error(w, err.Error(), http.StatusServiceUnavailable)
        return
    }
    http.Error(w, "internal error", http.StatusInternalServerError)
}
```

## Context Usage

### Request Context

```go
func Middleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        ctx := r.Context()
        ctx = context.WithValue(ctx, "request_id", generateID())
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

func Handler(w http.ResponseWriter, r *http.Request) {
    requestID := r.Context().Value("request_id").(string)
    // Use requestID for logging
}
```

## Graceful Shutdown

```go
func main() {
    // Setup server
    srv := &http.Server{Addr: ":8080", Handler: handler}
    
    // Start server in goroutine
    go func() {
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatal(err)
        }
    }()
    
    // Wait for interrupt signal
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit
    
    // Graceful shutdown
    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()
    
    if err := srv.Shutdown(ctx); err != nil {
        log.Fatal(err)
    }
}
```

## Testing Patterns

### Handler Testing

```go
func TestHealthCheck(t *testing.T) {
    req := httptest.NewRequest("GET", "/health", nil)
    w := httptest.NewRecorder()
    
    HealthCheck(w, req)
    
    if w.Code != http.StatusOK {
        t.Errorf("expected status 200, got %d", w.Code)
    }
}
```

### Middleware Testing

```go
func TestMiddleware(t *testing.T) {
    var called bool
    next := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        called = true
    })
    
    middleware := func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            next.ServeHTTP(w, r)
        })
    }
    
    handler := middleware(next)
    req := httptest.NewRequest("GET", "/", nil)
    handler.ServeHTTP(httptest.NewRecorder(), req)
    
    if !called {
        t.Error("next handler was not called")
    }
}
```
