import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';
import { getAuth, GoogleAuthProvider } from 'firebase/auth';
import firebaseConfig from '../config/firebase.json';

if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
}

export const auth = getAuth();
export const googleProvider = new GoogleAuthProvider();
export const uiConfig = {
  signInFlow: window.location.hostname === 'localhost' ? 'popup' : 'redirect',
  signInOptions: [GoogleAuthProvider.PROVIDER_ID],
  callbacks: { signInSuccessWithAuthResult: () => false },
};
