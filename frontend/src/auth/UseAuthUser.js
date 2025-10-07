import { useEffect, useState } from 'react';
import { auth } from './Firebase';

export function useAuthUser() {
  const [user, setUser] = useState(auth.currentUser);
  useEffect(() => auth.onAuthStateChanged(setUser), []);
  return user;
}
