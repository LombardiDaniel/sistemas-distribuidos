package main

import (
	"fmt"
	"sync"
	"time"
)

var (
	counter int = 0
	mu      sync.Mutex
)

func incrementCounterSafe() {
	mu.Lock()
	counter++
	mu.Unlock()
}

func incrementCounter() {
	counter++
}

func main() {
	for range 1000 {
		go incrementCounter()
		// go incrementCounterSafe()
	}

	time.Sleep(time.Second)
	fmt.Println("Final counter value:", counter)
}
