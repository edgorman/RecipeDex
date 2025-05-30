import { Box, Link, Typography } from '@material-ui/core';
import { Login } from './Login';

export function Header({user, onLogin}) {
  return (
    <Box className={"header"}>
      <Typography variant="subtitle1" className={"headerLogo"}>
        <Link href="/" underline="none" >RecipeDex</Link>
      </Typography>
      <Login user={user} onLogin={onLogin} />
    </Box>
  );
}
