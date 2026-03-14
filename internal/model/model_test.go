package model

import "testing"

func TestDomainError(t *testing.T) {
	err := NewDomainError("INVALID_ARG", "invalid argument", ErrInvalidArgument)

	if err.Code != "INVALID_ARG" {
		t.Errorf("expected code INVALID_ARG, got %s", err.Code)
	}
	if err.Message != "invalid argument" {
		t.Errorf("expected message 'invalid argument', got %s", err.Message)
	}
	if err.Error() != "invalid argument" {
		t.Errorf("expected Error() to return 'invalid argument', got %s", err.Error())
	}
}

func TestDomainErrorUnwrap(t *testing.T) {
	err := NewDomainError("INVALID_ARG", "invalid argument", ErrInvalidArgument)

	unwrapped := err.Unwrap()
	if unwrapped != ErrInvalidArgument {
		t.Errorf("expected unwrapped error to be ErrInvalidArgument")
	}
}

func TestResponseGeneric(t *testing.T) {
	resp := Response[string]{
		Success: true,
		Data:    "test data",
	}

	if !resp.Success {
		t.Error("expected Success to be true")
	}
	if resp.Data != "test data" {
		t.Errorf("expected data 'test data', got %s", resp.Data)
	}
}

func TestResponseError(t *testing.T) {
	resp := Response[string]{
		Success: false,
		Error:   "something went wrong",
	}

	if resp.Success {
		t.Error("expected Success to be false")
	}
	if resp.Error != "something went wrong" {
		t.Errorf("expected error 'something went wrong', got %s", resp.Error)
	}
}
