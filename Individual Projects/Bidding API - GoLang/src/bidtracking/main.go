package main

import (
	"database/sql"
	"encoding/json"
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
	_ "github.com/mattn/go-sqlite3"
)

type Config struct {
	Port   int
	Host   string
	Scheme string
}

var config Config
var database *sql.DB

func main() {

	database, _ = sql.Open("sqlite3", "./bidtracking.db")

	statement, _ := database.Prepare("CREATE TABLE IF NOT EXISTS bid (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT, user TEXT, value DECIMAL(10,5), unit TEXT)")
	statement.Exec()
	log.Println("Database opened")

	// var wait time.Duration
	configFile, _ := os.Open("config.json")
	decoder := json.NewDecoder(configFile)
	decoder.Decode(&config)
	router := mux.NewRouter()
	router.Host(config.Host)
	router.Schemes(config.Scheme)
	router.HandleFunc("/api/v1/getBidsForItem/{item}", GetBidsForItem).Methods("GET")
	router.HandleFunc("/api/v1/sendBidForItem", SendBidForItem).Methods("POST")
	router.HandleFunc("/api/v1/getWinningBidForItem/{item}", GetWinningBidForItem).Methods("GET")
	router.HandleFunc("/api/v1/getBidsOfUser/{user}", GetBidsOfUser).Methods("GET")

	log.Println("Listening at port 8000")
	log.Fatal(http.ListenAndServe(":8000", router))
}
