import { useEffect, useState } from 'react';
import { Container, Box, Typography } from '@material-ui/core';
import { getAuth, onAuthStateChanged, signInWithPopup, signOut, GoogleAuthProvider } from 'firebase/auth';
import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';

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

const firebaseConfig = require('./config/firebase.json');
if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
}
const firebaseAuth = getAuth();
const googleProvider = new GoogleAuthProvider();

export default function App() {
  const [user, setUser] = useState(null);
  const [recipe, setRecipe] = useState(null);
  const [chatInput, setChatInput] = useState("");
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(firebaseAuth, (firebaseUser) => {
      if (firebaseUser) {
        setUser({
          displayName: firebaseUser.displayName,
          email: firebaseUser.email,
          uid: firebaseUser.uid,
        });
      } else {
        setUser(null);
      }
    });

    return () => unsubscribe();
  }, []);

  const handleLogin = async () => {
    if (user) {
      await signOut(firebaseAuth);
    } else {
      try {
        await signInWithPopup(firebaseAuth, googleProvider);
      } catch (error) {
        console.error("Login failed:", error);
      }
    }
  };

  const handleSend = async () => {
    if (chatInput.trim()) {
      setMessages(prev => [...prev, { sender: "user", text: chatInput }]);
      setChatInput("");

      if (user !== null) {
        try {
          const token = await firebase.auth().currentUser.getIdToken();
          const response = await fetch(`${process.env.REACT_APP_BACKEND_API}/protected`, {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`,
              "Authorization-Provider": "firebase"
            },
          });

          if (!response.ok) {
            console.log(response);
            throw new Error(response.statusText);
          }

          const data = await response.json();
          console.log("successful response", data);
        } catch (error) {
          console.error("bad response", error);
        }
      }

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
      <Header user={user} onLogin={handleLogin} />
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
              Welcome {user ? (`back ${user.displayName}!`) : ("to RecipeDex!")}
            </Typography>
            <br />
            <Typography variant="subtitle1">
              Ask to generate a recipe,<br />or import one from a URL or image.
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
