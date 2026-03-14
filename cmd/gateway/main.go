package main

import (
	"context"
	"log"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/hardware-software-co-design/go-llm-gateway/internal/cgobridge"
	"github.com/hardware-software-co-design/go-llm-gateway/internal/config"
	"github.com/hardware-software-co-design/go-llm-gateway/internal/handlers"
	"github.com/hardware-software-co-design/go-llm-gateway/internal/middleware"
)

func main() {
	ctx := context.Background()

	_ = config.Load()

	slog.SetDefault(slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
		Level: slog.LevelInfo,
	})))

	slog.Info("Starting Go LLM Gateway", "version", "0.1.0")

	engine := cgobridge.NewEngine()

	router := http.NewServeMux()

	router.HandleFunc("/health", handlers.HealthCheck)
	router.HandleFunc("/ready", handlers.ReadyCheck)
	router.HandleFunc("/api/v1/chat", handlers.Chat(engine))

	handler := middleware.Chain(router,
		middleware.RequestID,
		middleware.Logger,
		middleware.Recover,
		middleware.CORS,
		middleware.RateLimit,
	)

	srv := &http.Server{
		Addr:         ":8080",
		Handler:      handler,
		ReadTimeout:  30 * time.Second,
		WriteTimeout: 30 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	go func() {
		slog.Info("Server starting on :8080")
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatal("Server error", "error", err)
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	slog.Info("Shutting down server...")

	shutdownCtx, cancel := context.WithTimeout(ctx, 10*time.Second)
	defer cancel()

	if err := srv.Shutdown(shutdownCtx); err != nil {
		slog.Error("Server shutdown error", "error", err)
	}

	engine.Destroy()

	slog.Info("Server stopped")
}
