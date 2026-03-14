# Go LLM Gateway - Testing Guide

## Test Overview

| Category | Count | Location |
|----------|-------|----------|
| Unit Tests | 10 | `internal/config/`, `internal/model/` |

## Running Tests

### Run All Tests

```bash
cd /Users/luisvalencia/Documents/go-llm-gateway
go test ./...
```

### Verbose Output

```bash
go test -v ./...
```

### Specific Package

```bash
go test -v ./internal/config/
go test -v ./internal/model/
```

### With Coverage

```bash
go test -cover ./...
```

## Test Structure

```
go-llm-gateway/
├── internal/
│   ├── config/
│   │   ├── config.go
│   │   └── config_test.go    # 6 tests
│   ├── model/
│   │   ├── model.go
│   │   ├── api.go
│   │   └── model_test.go     # 4 tests
│   ├── handlers/
│   ├── middleware/
│   └── cgobridge/
├── cmd/
└── tests/
```

## Test Descriptions

### config_test.go

| Test | Description |
|------|-------------|
| `TestLoadDefaults` | Test default configuration |
| `TestLoadEnvOverrides` | Test environment variable overrides |
| `TestGetEnvDefault` | Test default value for missing env |
| `TestGetEnvOverride` | Test value from env |
| `TestGetEnvInt` | Test integer parsing |
| `TestGetEnvIntDefault` | Test default for invalid int |

### model_test.go

| Test | Description |
|------|-------------|
| `TestDomainError` | Test error creation and properties |
| `TestDomainErrorUnwrap` | Test error unwrapping |
| `TestResponseGeneric` | Test generic response type |
| `TestResponseError` | Test error response |

## Writing Tests

### Basic Test

```go
package config

import "testing"

func TestExample(t *testing.T) {
    result := someFunction()
    if result != expected {
        t.Errorf("expected %v, got %v", expected, result)
    }
}
```

### Table-Driven Tests

```go
func TestGetEnvInt(t *testing.T) {
    tests := []struct {
        name     string
        key      string
        def      int
        envValue string
        expected int
    }{
        {"valid int", "TEST_KEY", 10, "42", 42},
        {"invalid int", "TEST_KEY", 10, "abc", 10},
        {"empty", "TEST_KEY", 10, "", 10},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if tt.envValue != "" {
                os.Setenv(tt.key, tt.envValue)
                defer os.Unsetenv(tt.key)
            }
            
            result := getEnvInt(tt.key, tt.def)
            if result != tt.expected {
                t.Errorf("expected %d, got %d", tt.expected, result)
            }
        })
    }
}
```

### HTTP Handler Tests

```go
package handlers

import (
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestHealthCheck(t *testing.T) {
    req := httptest.NewRequest("GET", "/health", nil)
    w := httptest.NewRecorder()
    
    HealthCheck(w, req)
    
    if w.Code != http.StatusOK {
        t.Errorf("expected status %d, got %d", http.StatusOK, w.Code)
    }
    
    // Parse response
    var resp model.HealthStatus
    if err := json.NewDecoder(w.Body).Decode(&resp); err != nil {
        t.Fatalf("failed to decode response: %v", err)
    }
    
    if resp.Status != "ok" {
        t.Errorf("expected status 'ok', got '%s'", resp.Status)
    }
}
```

### Middleware Tests

```go
package middleware

import (
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestLogger(t *testing.T) {
    var logged bool
    next := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        logged = true
    })
    
    handler := Logger(next)
    
    req := httptest.NewRequest("GET", "/test", nil)
    handler.ServeHTTP(httptest.NewRecorder(), req)
    
    if !logged {
        t.Error("next handler was not called")
    }
}
```

## Test Best Practices

### 1. Use Subtests

```go
func TestConfig(t *testing.T) {
    t.Run("defaults", func(t *testing.T) {
        // Test defaults
    })
    
    t.Run("overrides", func(t *testing.T) {
        // Test overrides
    })
}
```

### 2. Clean Up Resources

```go
func TestWithEnv(t *testing.T) {
    os.Setenv("TEST_KEY", "value")
    defer os.Unsetenv("TEST_KEY")
    
    // Test code
}
```

### 3. Test Error Cases

```go
func TestError(t *testing.T) {
    err := someFunctionThatErrors()
    if err == nil {
        t.Fatal("expected error")
    }
    
    if !errors.Is(err, expectedError) {
        t.Errorf("expected %v, got %v", expectedError, err)
    }
}
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Go
        uses: actions/setup-go@v5
        with:
          go-version: '1.26'
      
      - name: Test
        run: go test -v -race -cover ./...
```

## Benchmarking

```go
import "testing"

func BenchmarkInference(b *testing.B) {
    engine := NewEngine()
    defer engine.Destroy()
    
    prompt := "Hello, world!"
    
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        engine.Infer(prompt)
    }
}
```

Run benchmarks:
```bash
go test -bench=. -benchmem ./...
```
