import React from 'react';
import { getAuth } from 'firebase/auth';
import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';
import { AuthGate } from './components/AuthGate';
import EngineeringConsole from './components/EngineeringConsole';
import './App.css';

const firebaseConfig = require('./config/firebase.json');
if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
}
const firebaseAuth = getAuth();


export default function App() {
  const auth = firebaseAuth;
  const [user, setUser] = React.useState(auth.currentUser);
  React.useEffect(() => auth.onAuthStateChanged(setUser), [auth]);

  return (
    <div>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 12px', borderBottom: '1px solid #eee' }}>
        <strong>RecipeDex</strong>
        {user && (
          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <img src={user.photoURL || ''} alt="avatar" style={{ width: 28, height: 28, borderRadius: '50%' }} onError={(e) => (e.currentTarget.style.display = 'none')} />
            <span>{user.displayName || user.email}</span>
            <button onClick={() => auth.signOut()}>Sign out</button>
          </div>
        )}
      </header>
      <AuthGate>
        <EngineeringConsole />
      </AuthGate>
    </div>
  );
}
