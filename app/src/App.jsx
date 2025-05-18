import { useEffect, useState } from 'react';
import { initializeApp } from 'firebase/app';
import {
  getAuth,
  onAuthStateChanged,
  GoogleAuthProvider,
  signInWithRedirect,
  getRedirectResult,
  signOut,
} from 'firebase/auth';

// TODO: Replace with your Firebase project config
const firebaseConfig = require('./config/firebase.json');
firebaseConfig.authDomain = 'recipedex-dev--pr73-feat-firebase-auth-wfv9krld.web.app';

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

export default function FirebaseAuthRedirect() {
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);

  // Handle redirect result on mount
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (firebaseUser) => {
      setUser(firebaseUser);
    });

    // Also check for redirect errors
    getRedirectResult(auth).catch((err) => {
      if (err) setError(err);
    });

    return () => unsubscribe();
  }, []);

  const handleLogin = () => {
    signInWithRedirect(auth, provider);
  };

  const handleLogout = () => {
    signOut(auth);
  };

  return (
    <div className="p-4 max-w-sm mx-auto border rounded">
      {error && <p className="text-red-500">Error: {error.message}</p>}
      {user ? (
        <div>
          <p>Welcome, {user.displayName}</p>
          <button onClick={handleLogout} className="mt-2 px-4 py-2 bg-gray-200 rounded">
            Logout
          </button>
        </div>
      ) : (
        <button onClick={handleLogin} className="px-4 py-2 bg-blue-500 text-white rounded">
          Sign in with Google
        </button>
      )}
    </div>
  );
}
