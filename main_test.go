package main

import (
	"context"
	"net/http"
	"net/http/httptest"
	"os"
	"testing"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
)

var mockAuthServer *httptest.Server
var mockContext context.Context

func mockServers() {
	mockAuthServer = httptest.NewServer(
		http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			if r.URL.Path == "/apis/v1/me" {
				if r.Header.Get("Authorization") == "Bearer valid_token" {
					w.Header().Add("Content-Type", "application/json")
					w.Write([]byte(`{"uuid": "00000000-0000-0000-0000-000000000000", "email": "test@email.com", "username": "TestUsername"}`))
				} else {
					w.WriteHeader(http.StatusUnauthorized)
				}
			}
		}),
	)

	os.Setenv("LYNLAB_AUTH_HOST", mockAuthServer.URL)
	db.Save(&User{ID: "00000000-0000-0000-0000-000000000000", IsAdmin: true})
}

func TestMain(m *testing.M) {
	cleanModels()
	migrateModels()
	mockServers()
	defer cleanModels()

	mockContext = context.Background()
	mockContext = context.WithValue(mockContext, ctxAuthToken, "Bearer valid_token")
	mockContext = context.WithValue(mockContext, ctxClientIP, "127.0.0.1")

	m.Run()
}

func TestAll(t *testing.T) {
	RegisterFailHandler(Fail)
	RunSpecs(t, "All Suite")
}
