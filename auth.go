package main

import (
	"encoding/json"
	"net/http"
	"os"
	"time"
)

var httpClient = &http.Client{
	Timeout: 5 * time.Second,
}

type AuthResponse struct {
	UUID     string
	Username string
	Email    string
}

func Authenticate(token string) (*AuthResponse, error) {
	host, ok := os.LookupEnv("LYNLAB_AUTH_HOST")
	if !ok {
		host = "https://auth.lynlab.co.kr"
	}

	req, _ := http.NewRequest("GET", host+"/apis/v1/me", nil)
	req.Header.Set("Authorization", token)

	res, err := httpClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer res.Body.Close()

	if res.StatusCode != http.StatusOK {
		return nil, ErrForbidden
	}

	var body AuthResponse
	err = json.NewDecoder(res.Body).Decode(&body)
	if err != nil {
		return nil, err
	}
	return &body, nil
}
