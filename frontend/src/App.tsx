import { Switch } from "wouter";
import { Router, Route, } from "wouter";
import Home from "./Home";
import MarioAI from "./MarioAI";
import MarioGame from "./components/MarioGame";

export default function App() {
  return (
    <Switch>

      <Router base="/">
        <Route path="/" component={Home}></Route>
        <Route path="/home" component={Home}></Route>
        <Route path="/game" component={MarioGame}></Route>
        <Route path="/AI" component={MarioAI}></Route>

      </Router>

    </Switch>
  )
}

