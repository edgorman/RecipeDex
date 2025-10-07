import '@material/web/icon/icon.js';
import '@material/web/iconbutton/icon-button.js';
import '@material/web/button/filled-button.js';
import '@material/web/dialog/dialog.js';
import '@material/web/button/text-button.js';

import StyledFirebaseAuth from 'react-firebaseui/StyledFirebaseAuth';
import { auth, uiConfig } from '../../auth/Firebase';
import { useAuthUser } from '../../auth/UseAuthUser';
import '../../auth/Firebase.css';
import { useTheme } from '../../style/UseTheme';
import { useRef, useCallback, useState } from 'react';
import { Link } from 'react-router-dom';

export function Navbar() {
  const user = useAuthUser();
  const { toggle } = useTheme();
  const dialogRef = useRef(null);
  const [shouldRenderFirebaseAuth, setShouldRenderFirebaseAuth] = useState(false);

  const openUserDialog = useCallback(() => {
    if (dialogRef.current) {
      if (typeof dialogRef.current.show === 'function') {
        dialogRef.current.show();
      } else {
        dialogRef.current.setAttribute('open', '');
      }
      // Once opened, allow FirebaseUI to render (one-way flag)
      if (!shouldRenderFirebaseAuth) {
        setShouldRenderFirebaseAuth(true);
      }
    }
  }, [shouldRenderFirebaseAuth]);

  const closeUserDialog = useCallback(() => {
    if (dialogRef.current) {
      if (typeof dialogRef.current.close === 'function') {
        dialogRef.current.close();
      } else {
        dialogRef.current.removeAttribute('open');
      }
    }
  }, []);

  return (
    <header style={{ display: 'flex', gap: 16, justifyContent: 'space-between', alignItems: 'center', padding: '8px 12px' }}>
      <h3>
        <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
          RecipeDex
        </Link>
      </h3>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <md-icon-button onClick={toggle} aria-label="Toggle light/dark mode">
          <md-icon>routine</md-icon>
        </md-icon-button>
        <md-icon-button onClick={openUserDialog} aria-label="User menu" >
          <md-icon>person_2</md-icon>
        </md-icon-button>

        <md-dialog ref={dialogRef} aria-label="User dialog">
          <div slot="headline">
            {user ? `Welcome back!` : "Sign up or log in"}
          </div>
          <form slot="content" method="dialog">
            {
              user ?
                (
                  <md-list>
                    <md-list-item>
                      You are signed in as <b>{user.displayName}</b>.
                    </md-list-item>
                    <md-list-item
                      type="link"
                      href="/user/me">
                      <div slot="headline">Your profile</div>
                      <md-icon slot="end">person_2</md-icon>
                    </md-list-item>
                    <md-list-item
                      type="link"
                      href="/user/me/recipes">
                      <div slot="headline">Your recipes</div>
                      <md-icon slot="end">menu_book</md-icon>
                    </md-list-item>
                  </md-list>
                ) :
                (
                  <md-list>
                    <md-list-item>
                      Please choose one of the options below
                    </md-list-item>
                    <md-list-item>
                      {shouldRenderFirebaseAuth && (
                        <StyledFirebaseAuth uiConfig={uiConfig} firebaseAuth={auth} />
                      )}
                    </md-list-item>
                  </md-list>
                )
            }
          </form>
          <div slot="actions">
            {user && (
              <md-filled-button aria-label="Sign out" onClick={() => auth.signOut()}>Sign Out</md-filled-button>
            )}
            <md-text-button value="cancel" onClick={closeUserDialog}>Close</md-text-button>
          </div>
        </md-dialog>
      </div>
    </header>
  );
}
