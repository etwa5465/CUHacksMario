import { navigate } from "wouter/use-browser-location";
import "./style.css"


export default function Home() {
    return (
        <div>
            <div className="background">
                <h1 className="text-container">Leveling Up Efficiency</h1>
            </div>
            <hr />
            <div className="center-container">
                <div className="box">
                    <p className="p">
                        <strong>What the Game Is: </strong> <br />
                        Our project is a platformer game inspired by classics like Mario,
                        enhanced with a machine learning (ML) optimization feature. Players
                        guide a character through levels filled with obstacles and enemies,
                        aiming to reach a flag. The ML component provides an innovative
                        twist by analyzing the level and suggesting the most efficient path,
                        merging traditional gameplay with modern AI-driven insights.
                    </p>
                </div>
            </div>
            <div className="center-container">
                <div className="box">
                    <p className="p">
                        <strong>How the Game Works: </strong> <br />
                        The front-end, built with HTML, CSS, and React, delivers a
                        responsive and interactive game environment. The back-end, powered
                        by Python, integrates an ML model using libraries like TensorFlow or
                        PyTorch to analyze level layouts and player behavior. This model
                        calculates and displays the optimal route to the flag, offering both
                        an engaging gameplay experience and a practical demonstration of
                        AI-driven pathfinding algorithms.
                    </p>
                </div>
            </div>
            <button className="button" onClick={() => navigate("game")}>
                <p className="p2">Next Page</p>
            </button>
        </div>
    );
}

