import './App.css';
import { Routes, Route } from 'react-router-dom';
import { Navbar } from './navbar/Index';
import { DeveloperConsole } from './developer/Index'
import { ErrorNotFound } from './error/NotFound';
import { RecipeIndex } from './recipe/Index';
import { RecipeList } from './recipe/List';
import { UserIndex } from './user/Index';

export default function App() {

  return (
    <div className="app">
      <Navbar />
      <Routes>
        <Route path="/" element={<RecipeList />} />
        <Route path="/recipe/:id" element={<RecipeIndex />} />
        <Route path="/user/:id" element={<UserIndex />} />
        <Route path="/developer" element={<DeveloperConsole />} />
        <Route path="*" element={<ErrorNotFound />} />
      </Routes>
    </div>
  );
}
