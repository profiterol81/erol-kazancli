package main

import (
	"encoding/json"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

// Bid Structure
type Bid struct {
	Item  string  `json:"item" description:"item name for the bid"`
	User  string  `json:"user" description:"user who bids on the item"`
	Value float32 `json:"value" description:"the value of the bid of the user on the item"`
	Unit  string  `json:"unit" description:"Unit of the bid"`
}

// Error structure
type Message struct {
	ErrorCode int    `json:"errorCode" description:"Code of the error"`
	Title     string `json:"message,omitempty" description:"Title of the error"`
}

// Gets all bids for an item
func GetBidsForItem(w http.ResponseWriter, r *http.Request) {

	log.Println("Reading")
	bids := make([]Bid, 0)
	log.Println(mux.Vars(r)["item"])
	rows, err := database.Query("SELECT item, user, value, unit FROM bid WHERE item = ?", mux.Vars(r)["item"])
	if err != nil {
		log.Println(err.Error())
	}
	for rows.Next() {
		var bid Bid
		rows.Scan(&bid.Item, &bid.User, &bid.Value, &bid.Unit)
		bids = append(bids, bid)
	}
	log.Println("Read complete")

	json.NewEncoder(w).Encode(bids)
}

// Gets the winning bid for an item
func GetWinningBidForItem(w http.ResponseWriter, r *http.Request) {
	log.Println("Reading winning bid")
	log.Println(mux.Vars(r)["item"])
	rows, err := database.Query("SELECT item, user, value, unit FROM bid WHERE item = ?", mux.Vars(r)["item"])
	if err != nil {
		json.NewEncoder(w).Encode(Message{
			ErrorCode: 1,
			Title:     "Failed to select bids",
		})
		return
	}
	defer rows.Close()

	var maxBid Bid
	for rows.Next() {
		var bid Bid
		rows.Scan(&bid.Item, &bid.User, &bid.Value, &bid.Unit)
		if bid.Value > maxBid.Value {
			maxBid = bid
		}
	}
	log.Println("Read Complete")

	json.NewEncoder(w).Encode(maxBid)
}

// Gets all bids of a user
func GetBidsOfUser(w http.ResponseWriter, r *http.Request) {
	log.Println("Reading bids of user")
	bids := make([]Bid, 0)
	log.Println(mux.Vars(r)["user"])
	rows, err := database.Query("SELECT item, user, value, unit FROM bid WHERE user = ?", mux.Vars(r)["user"])
	if err != nil {
		json.NewEncoder(w).Encode(Message{
			ErrorCode: 1,
			Title:     "Failed to add bid",
		})
		return
	}
	defer rows.Close()
	for rows.Next() {
		var bid Bid
		rows.Scan(&bid.Item, &bid.User, &bid.Value, &bid.Unit)
		bids = append(bids, bid)
	}
	log.Println("Read complete")

	json.NewEncoder(w).Encode(bids)
}

// Sends a bid of a user for an item
func SendBidForItem(w http.ResponseWriter, r *http.Request) {

	log.Println("Sending bid")
	var bid Bid

	err := json.NewDecoder(r.Body).Decode(&bid)
	if err != nil {
		json.NewEncoder(w).Encode(Message{
			ErrorCode: 1,
			Title:     "Failed to add bid",
		})
		return
	}

	log.Println(bid.Item)
	statement, _ := database.Prepare("INSERT INTO bid (item, user, value, unit) VALUES (?, ?, ?, ?)")
	statement.Exec(bid.Item, bid.User, bid.Value, bid.Unit)

	log.Println("Bid sent")
	json.NewEncoder(w).Encode(Message{
		ErrorCode: 0,
		Title:     "Bid successfully added",
	})
}
