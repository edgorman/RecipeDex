import React from 'react';
import StyledFirebaseAuth from 'react-firebaseui/StyledFirebaseAuth';
import { getAuth, GoogleAuthProvider } from 'firebase/auth';
import 'firebaseui/dist/firebaseui.css';

const uiConfig = {
  signInFlow: 'popup',
  signInOptions: [
    GoogleAuthProvider.PROVIDER_ID,
  ],
  callbacks: {
    // Avoid redirect after sign-in.
    signInSuccessWithAuthResult: () => false,
  },
};

export function AuthGate({ children }) {
  const auth = getAuth();
  const [user, setUser] = React.useState(auth.currentUser);
  React.useEffect(() => {
    return auth.onAuthStateChanged(setUser);
  }, [auth]);

  if (!user) {
    return (
      <div style={{ maxWidth: 420, margin: '10vh auto', padding: 24 }}>
        <h2>Sign in to RecipeDex</h2>
        <StyledFirebaseAuth uiConfig={uiConfig} firebaseAuth={auth} />
      </div>
    );
  }

  return children;
}
