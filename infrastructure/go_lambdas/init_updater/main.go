package main

import (
	"bytes"
	"fmt"
	"net/http"
)

func main() {
	url := "http://backend:8000/cryptos/update"
	payload := []byte(`{}`)

	resp, err := http.Post(url, "application/json", bytes.NewBuffer(payload))
	if err != nil {
		fmt.Println("❌ Failed to call backend:", err)
		return
	}
	defer resp.Body.Close()

	fmt.Println("✅ Called /cryptos/update, status:", resp.Status)
}