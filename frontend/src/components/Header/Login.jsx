import { IconButton } from '@material-ui/core';
import ExitToAppIcon from '@material-ui/icons/ExitToApp';
import { default as PersonIcon } from '@material-ui/icons/Person';

export function Login({user, onLogin}) {
  return (
    <IconButton color="default" onClick={onLogin}>
      {user ? <PersonIcon /> : <ExitToAppIcon />}
    </IconButton>
  );
}
