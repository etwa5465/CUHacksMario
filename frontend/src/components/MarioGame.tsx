import React, { useEffect, useRef, useState } from 'react';
import Phaser from 'phaser';
import { navigate } from 'wouter/use-browser-location';

const MarioGame: React.FC = () => {
  const gameContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!gameContainerRef.current) return;

    const config: Phaser.Types.Core.GameConfig = {
      type: Phaser.AUTO,
      width: 800,
      height: 600,
      parent: gameContainerRef.current,
      physics: {
        default: 'arcade',
        arcade: {
          gravity: { x: 0, y: 300 },
          debug: false,
        },
      },
      scene: {
        preload: preload,
        create: create,
        update: update,
      },
    };

    const game = new Phaser.Game(config);

    let player: Phaser.Physics.Arcade.Sprite;
    let goomba: Phaser.Physics.Arcade.Sprite;
    let goomba2: Phaser.Physics.Arcade.Sprite;
    let platforms: Phaser.Physics.Arcade.StaticGroup;
    let cursors: Phaser.Types.Input.Keyboard.CursorKeys | undefined;

    function preload(this: Phaser.Scene) {
      // Load assets
      this.load.image('sky', 'https://labs.phaser.io/assets/skies/space3.png');
      this.load.image('ground', 'https://labs.phaser.io/assets/platforms/grass-tile.png');
      this.load.image('star', 'https://labs.phaser.io/assets/sprites/star.png');
      this.load.image('flag', '/flag.png')
      this.load.spritesheet('mario', '/mario.png', {
        frameWidth: 40,
        frameHeight: 40,
      });
      this.load.spritesheet('imario', '/imario.png', {
        frameWidth: 40,
        frameHeight: 40,
      });
      this.load.spritesheet('goomba', '/goomba.png', {
        frameWidth: 40,
        frameHeight: 40,
      });
    }

    function create(this: Phaser.Scene) {
      // Focus the game canvas
      this.game.canvas.setAttribute('tabindex', '0');
      this.game.canvas.focus();

      // Enable keyboard input
      if (this.input.keyboard) {
        this.input.keyboard.enabled = true;
      }


      // Initialize cursors
      if (this.input.keyboard) {
        cursors = this.input.keyboard.createCursorKeys();
      } else {
        console.warn('Keyboard input not available.');
      }

      // Add background
      this.add.image(400, 300, 'sky');

      // Create platforms
      platforms = this.physics.add.staticGroup();
      platforms.create(400, 568, 'ground').setScale(2).refreshBody();
      platforms.create(600, 400, 'ground');
      platforms.create(100, 330, 'ground');
      platforms.create(430, 200, 'ground').setScale(3).refreshBody();
      platforms.create(750, 220, 'ground');

      //Create flag
      const flag = this.physics.add.sprite(100, 313, 'flag');
      flag.setOrigin(0.5, 1);
      flag.body.setAllowGravity(false);

      //create goombas

      goomba = this.physics.add.sprite(200, 460, 'goomba');
      goomba.setBounce(0.2);
      goomba.setCollideWorldBounds(true);

      goomba2 = this.physics.add.sprite(430, 100, 'goomba');
      goomba2.setBounce(0.2);
      goomba2.setCollideWorldBounds(true);

      // Create player
      player = this.physics.add.sprite(100, 450, 'mario');
      player.setBounce(0.2);
      player.setCollideWorldBounds(true);

      // Player animations
      this.anims.create({
        key: 'left',
        frames: this.anims.generateFrameNumbers('imario', { start: 0, end: 1 }),
        frameRate: 10,
        repeat: -1,
      });

      this.anims.create({
        key: 'right',
        frames: this.anims.generateFrameNumbers('mario', { start: 0, end: 1 }),
        frameRate: 10,
        repeat: -1,
      });

      // Collide player with platforms
      this.physics.add.collider(player, platforms);

      // Collide goombas with platforms
      this.physics.add.collider(goomba, platforms);
      this.physics.add.collider(goomba2, platforms);

      const flagtouch = false;
      const goombatouch = false;

      if (!goombatouch) {
        // Detect collision between player and flag
        this.physics.add.overlap(player, flag, () => {
          // Freeze Mario
          player.setVelocity(0, 0);
          player.anims.stop(); // Stop animations
          player.setTint(0x00ff00); // Optional: Add a visual effect (e.g., tint Mario green)

          // Display "Level Over" message
          const levelOverText = this.add.text(400, 300, 'Level Over', {
            fontSize: '48px',
            color: '#ffffff',
            fontFamily: 'Arial',
          });
          levelOverText.setOrigin(0.5, 0.5); // Center the text
        });
      }


      if (!flagtouch) {
        // Detect collision between player and goomba
        this.physics.add.overlap(player, goomba, () => {
          // Freeze Mario
          player.setVelocity(0, 0);
          player.anims.stop(); // Stop animations
          player.setTint(0xB22222); // Optional: Add a visual effect (e.g., tint Mario red)

          // Display "Level Over" message
          const levelOverText = this.add.text(400, 300, 'Level Over', {
            fontSize: '48px',
            color: '#ffffff',
            fontFamily: 'Arial',
          });
          levelOverText.setOrigin(0.5, 0.5); // Center the text
        });

        this.physics.add.overlap(player, goomba2, () => {
          // Freeze Mario
          player.setVelocity(0, 0);
          player.anims.stop(); // Stop animations
          player.setTint(0xB22222); // Optional: Add a visual effect (e.g., tint Mario red)

          // Display "Level Over" message
          const levelOverText = this.add.text(400, 300, 'Level Over', {
            fontSize: '48px',
            color: '#ffffff',
            fontFamily: 'Arial',
          });
          levelOverText.setOrigin(0.5, 0.5); // Center the text
        });
      }

    }


    function update(this: Phaser.Scene) {
      if (cursors && player.body) {
        // Debug logs
        console.log('Left:', cursors.left.isDown);
        console.log('Right:', cursors.right.isDown);
        console.log('Up:', cursors.up.isDown);





        // Move Left
        if (cursors.left.isDown) {
          player.setVelocityX(-160);
          player.anims.play('left', true);
        }
        // Move Right
        else if (cursors.right.isDown) {
          player.setVelocityX(160);
          player.anims.play('right', true);
        }
        // Stop Moving
        else {
          player.setVelocityX(0);
        }

        // Jump
        if (cursors.up.isDown && player.body.blocked.down) {
          player.setVelocityY(-330);
        }
      }
    }

    // Cleanup game on component unmount
    return () => {
      game.destroy(true);
    };
  }, []);



  return (
    <div>
      <div className="background">
        <h1 className="text-container">AstroMario Game</h1>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr" }}>
        <div ref={gameContainerRef} ></div>
        <div>
          <button className="button" onClick={() => navigate("AI")}><p className="p2">View AI</p></button>
          <div style={{ textAlign: "right", marginTop: "50px" }}>
            <a
              href="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
              target="_blank"
              rel="noopener noreferrer"
              style={{
                display: "inline-block",
                fontSize: "18px",
                backgroundColor: "#ff4757",
                color: "white",
                textDecoration: "none",
                borderRadius: "5px",
                cursor: "pointer",
              }}
            >
              Click for a surprise! 🎁
            </a>
          </div>
        </div>

      </div>






    </div>
  )



};

export default MarioGame;