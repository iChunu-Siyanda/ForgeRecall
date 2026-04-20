"use client";

import { useEffect, useState } from "react";

export default function StudyPage() {
  const [cards, setCards] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [loading, setLoading] = useState(true);
  const [history, setHistory] = useState([]);
  const [stats, setStats] = useState({
    easy: 0,
    medium: 0,
    hard: 0,
  });
  const [decks, setDecks] = useState([]);
  const [selectedDeck, setSelectedDeck] = useState(null);

  // Fetch decks for dropdown
  useEffect(() => {
    fetch("http://localhost:8000/study/decks/")
      .then((res) => res.json())
      .then((data) => setDecks(data))
      .catch((err) => console.error("Error fetching decks:", err));
  }, []);

  // Fetch due cards
  useEffect(() => {
    fetch("http://localhost:8000/study/due-cards/")
      .then((res) => res.json())
      .then((data) => {
        setCards(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching cards:", err);
        setLoading(false);
      });
  }, []);

  // Fetch cards for selected deck
  const fetchDeckCards = (deckId=null) => {
    if (!selectedDeck && deckId === null) return;
    let url = `http://localhost:8000/study/due-cards/?deck_id=${selectedDeck?.id || deckId}`;
    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        setCards(data);
        setCurrentIndex(0);
        setFlipped(false);
        setHistory([]);
        setStats({ easy: 0, medium: 0, hard: 0 });
      })
      .catch((err) => console.error("Error fetching deck cards:", err));
  };

  useEffect(() => {
    // if (selectedDeck) {
    //   fetchDeckCards(selectedDeck.id);
    // }
    fetchDeckCards();
  }, []);

  //Handle Deck Change
  const handleDeckChange = (deckId) =>  {
    const deck = decks.find((d) => d.id === parseInt(deckId));
    setSelectedDeck(deck);
    fetchDeckCards(deckId);
  };

  // Handle review
  const handleReview = async (rating) => {
    const card = cards[currentIndex];

    try {
      await fetch("http://localhost:8000/study/review-card/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          card_id: card.id,
          rating: rating,
        }),
      });

      // Record Prev Card
      setHistory((prev) => [...prev, currentIndex]);

      // Move to next card
      setFlipped(false);
      setCurrentIndex((prev) => prev + 1);

      // Update stats
      setStats((prev) => ({
        ...prev,
        easy: rating === 3 ? prev.easy + 1 : prev.easy,
        medium: rating === 2 ? prev.medium + 1 : prev.medium,
        hard: rating === 1 ? prev.hard + 1 : prev.hard,
      }));
    } catch (error) {
      console.error("Review failed:", error);
    }
  };

  // Handle previous card
  const handlePrevious = () => {
    if (history.length === 0) return;

    const prevIndex = history[history.length - 1];

    setHistory((prev) => prev.slice(0, -1));
    setCurrentIndex(prevIndex);
    setFlipped(false);
  };

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (!flipped) return;

      if (e.key === "1") handleReview(1);
      if (e.key === "2") handleReview(2);
      if (e.key === "3") handleReview(3);
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [flipped, currentIndex, cards]);

  // States
  if (loading) return <div className="text-white">Loading...</div>;

  // End of session screen
  if (currentIndex >= cards.length) {
    return (
      <div className="h-screen flex flex-col items-center justify-center bg-black text-white gap-6">
        <h1 className="text-2xl font-bold">Session Complete</h1>

        <div className="text-lg">
          ✅ Easy: {stats.easy}
          ⚠️ Medium: {stats.medium}❌ Hard: {stats.hard}
        </div>

        <button
          onClick={() => {
            setCurrentIndex(0);
            setStats({ easy: 0, medium: 0, hard: 0 });
            setHistory([]);
          }}
          className="bg-blue-500 px-6 py-2 rounded-lg"
        >
          Restart Session
        </button>
      </div>
    );
  }

  const card = cards[currentIndex];

  return (
    <div className="h-screen flex flex-col items-center justify-center bg-black text-white px-4">
      {/* Deck Selector */}
      <div className="mb-6">
        <select
          value={selectedDeck ? selectedDeck.id : ""}
          onChange={(e) => handleDeckChange(e.target.value)}
          className="bg-gray-700 text-white px-4 py-2 rounded-lg"
        >
          <option value="">All Decks</option>
          {decks.map((deck) => (
            <option key={deck.id} value={deck.id}>
              {deck.name}
            </option>
          ))}
        </select>
      </div>

      {/* Progress */}
      <div className="mb-4 text-sm text-gray-400">
        {currentIndex + 1} / {cards.length}
      </div>

      {/* Card */}
      <div
        className="bg-gray-800 p-10 rounded-2xl shadow-xl text-center max-w-xl w-full cursor-pointer transition"
        onClick={() => setFlipped(!flipped)}
      >
        {!flipped ? card.question : card.answer}
      </div>

      {/* Explanation (optional) */}
      {flipped && card.explanation && (
        <div className="mt-4 text-gray-400 text-sm max-w-xl text-center">
          {card.explanation}
        </div>
      )}

      {/* Buttons */}
      {flipped && (
        <div className="flex gap-4 mt-6">
          <button
            onClick={() => handleReview(1)}
            className="bg-red-500 px-4 py-2 rounded-lg"
          >
            Hard (1)
          </button>

          <button
            onClick={() => handleReview(2)}
            className="bg-yellow-500 px-4 py-2 rounded-lg"
          >
            Medium (2)
          </button>

          <button
            onClick={() => handleReview(3)}
            className="bg-green-500 px-4 py-2 rounded-lg"
          >
            Easy (3)
          </button>
        </div>
      )}

      {/* Previous Button */}
      {history.length > 0 && (
        <button
          onClick={handlePrevious}
          className="absolute top-4 left-4 bg-gray-700 px-3 py-1 rounded-lg text-sm"
        >
          Previous
        </button>
      )}
    </div>
  );
}
