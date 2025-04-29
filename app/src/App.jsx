import React, { useState } from 'react';
// import { useNavigate } from "react-router-dom";
import { Container, Box, Typography } from '@material-ui/core';
import { Header } from './components/Header/Header';
import { Recipe } from './components/Recipe/Recipe';
import { Chat } from './components/Chat/Chat';
import './App.css';

const sampleRecipe = {
  name: "Potato Leek Frittata",
  description: "A simple and delicious frittata made with potatoes and leeks.",
  serves: 4,
  prepTime: "15 minutes",
  cookTime: "30 minutes",
  totalTime: "45 minutes",
  difficulty: "Easy",
  cuisine: "French",
  dietaryRestrictions: ["Vegetarian", "Gluten-Free"],
  ingredients: ["1 potato", "1 leek", "5 eggs"],
  instructions: [
    "cut the potato", "cut the leek", "fry it all", "profit",
    "cut the potato", "cut the leek", "fry it all", "profit"
  ]
};

const sampleUser = {
  id: "123",
  name: "Edward",
  email: "user@example.com"
}

export default function App() {
  // const navigate = useNavigate();

  const [user, setUser] = useState(null);
  const [recipe, setRecipe] = useState(null);
  const [chatInput, setChatInput] = useState("");
  const [messages, setMessages] = useState([]);

  const handleLogin = () => {
    if (user !== null) {
      // navigate("/user");
      setUser(null);
    } else {
      // navigate("/login");
      setUser(sampleUser);
    }
  };

  const handleSend = () => {
    if (chatInput.trim()) {
      setMessages(prev => [...prev, { sender: "user", text: chatInput }]);
      setChatInput("");
      setTimeout(() => {
        setRecipe(sampleRecipe);
        setMessages(prev => [...prev, { sender: "ai", text: "Here's a suggestion to tweak your recipe." }]);
      }, 1000);
    }
  };

  const handleIngredientChange = (index, value) => {
    const newIngredients = [...recipe.ingredients];
    newIngredients[index] = value;
    setRecipe({ ...recipe, ingredients: newIngredients });
  };

  const handleInstructionChange = (index, value) => {
    const newInstructions = [...recipe.instructions];
    newInstructions[index] = value;
    setRecipe({ ...recipe, instructions: newInstructions });
  };

  return (
    <Container className="container" maxWidth="sm">
      <Header 
        user={user}
        onLogin={handleLogin}
      />
      <Box className="content" justifyContent={recipe ? "flex-start" : "center"}>
        {recipe ? (
          <Recipe 
            recipe={recipe} 
            onIngredientChange={handleIngredientChange}
            onInstructionChange={handleInstructionChange}
          />
        ) : (
          <>
            <Typography variant="subtitle1">
              Welcome {user ? (
                `back ${user.name}!`
              ) : (
                "to RecipeDex!"
              )}
            </Typography>
            <br/>
            <Typography variant="subtitle1">
              Ask to generate a recipe,<br/>or import one from a URL or image.
            </Typography>
          </>
        )}
      </Box>
      <Chat 
        chatInput={chatInput}
        onInputChange={setChatInput}
        onSend={handleSend}
        messages={messages.slice(-2)}
      />
    </Container>
  );
}
