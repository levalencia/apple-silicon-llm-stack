package handlers

import (
	"encoding/json"
	"net/http"

	"github.com/hardware-software-co-design/go-llm-gateway/internal/cgobridge"
	"github.com/hardware-software-co-design/go-llm-gateway/internal/model"
)

func HealthCheck(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(model.Response[model.HealthStatus]{
		Success: true,
		Data:    model.HealthStatus{Status: "ok"},
	})
}

func ReadyCheck(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(model.Response[model.HealthStatus]{
		Success: true,
		Data:    model.HealthStatus{Status: "ready"},
	})
}

func Chat(engine *cgobridge.Engine) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		var req struct {
			Prompt string `json:"prompt"`
		}

		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			http.Error(w, "Invalid request", http.StatusBadRequest)
			return
		}

		result := engine.Eval(req.Prompt)

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(model.Response[string]{
			Success: true,
			Data:    result,
		})
	}
}
