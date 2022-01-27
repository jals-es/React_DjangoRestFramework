import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import 'alertifyjs/build/css/alertify.css';
import './App.css';
import AuthRoute from "./components/AuthRoute"
import Spinner from './components/spinner';
import { Suspense } from 'react'
export default function App() {
  const Home = React.lazy(() => import("./pages/Home"));
  const Login = React.lazy(() => import("./pages/Auth/login"));
  const Register = React.lazy(() => import("./pages/Auth/register"));
  const Err404 = React.lazy(() => import("./pages/Err404"));
  return ( 
    <Router>
      <Routes>
        <Route path="/" element={<Suspense fallback={<Spinner/>}><AuthRoute><Home/></AuthRoute></Suspense>}/>
        <Route path="/login/" element={<Suspense fallback={<Spinner/>}><Login/></Suspense>} />
        <Route path="/register/" element={<Suspense fallback={<Spinner/>}><Register/></Suspense>} />
        <Route path="*" element={<Suspense fallback={<Spinner/>}><Err404/></Suspense>}/>
      </Routes>
    </Router>
  );
}