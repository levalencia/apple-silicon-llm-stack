# Go LLM Gateway Agent Instructions

You are an expert Go developer working on the `go-llm-gateway` repository. This project is a high-performance REST API gateway connecting HTTP clients (via Server-Sent Events) to a C++ Metal inference engine via CGO.

## 1. Build, Lint, and Test Commands

When you modify code, always self-verify using these commands from the `go-llm-gateway` directory:

- **Build**: `go build -o gateway ./cmd/gateway`
- **Lint**: `go vet ./...` (Use this strictly to ensure no errors are introduced)
- **Run all tests**: `go test ./... -v`
- **Run single test**: `go test ./internal/path/to/pkg -v -run ^TestFunctionName$`
- **Test with data race detection**: `go test -race ./...`

**Note on CGO**: Running code that imports `internal/cgobridge` requires a C++ compiler (`clang` or `gcc`) in the environment.

## 2. Architectural Guidelines

- **Standard Library Only**: (ADR-001) This project enforces strict usage of standard libraries only. Do NOT introduce third-party libraries (e.g., Gin, Echo, Logrus). 
- **Logging**: Use standard `log/slog` for structured logging.
- **Middleware Pattern**: Follow the Chain of Responsibility pattern for HTTP middleware. See `internal/middleware/`.
- **Graceful Shutdown**: Always ensure `http.Server` shuts down gracefully via signal catching and context (`srv.Shutdown(ctx)`).

## 3. Code Style & Best Practices

### Formatting and Imports
- Format all Go code using `gofmt`. Your edits must preserve standard Go indentation (tabs, not spaces).
- Group imports into two blocks: Standard Library first, then internal project imports.

### Error Handling
- Errors are values. Always explicitly check `if err != nil`. 
- NEVER use `panic()` except in `main()` during initialization or within a `recover` middleware.
- Return meaningful wrapped errors (e.g., `fmt.Errorf("failed to parse config: %w", err)`). Do not swallow errors.

### CGO and Interop
- CGO code in `internal/cgobridge` bridges Go and the C++ Engine. Be hyper-aware of memory boundaries.
- Ensure that memory allocated in C is explicitly freed. Use `defer` combined with cleanup methods when invoking C++ pointers.

### Testing Rules
- Use table-driven tests for comprehensive unit testing (see existing files in `internal/model/model_test.go`).
- Do not import testing frameworks like testify/assert. Use standard `if got != want { t.Errorf(...) }`.

## 4. Agent Operations
- Read `docs/ARCHITECTURE.md` and `docs/DESIGN.md` if you are modifying complex components.
- Use `glob` and `grep` to find existing implementations before creating new ones.
- Keep responses concise. Execute code changes directly when you have enough context.
