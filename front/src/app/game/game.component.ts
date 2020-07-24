import { Component, OnInit } from '@angular/core';
import {GameService} from '../../services/game.service';
import {Router} from '@angular/router';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.css']
})
export class GameComponent implements OnInit {

  images: string[];
  yearGuess: number;
  score: number;
  currentRound: number;
  buttonDisabled: boolean;
  countImg: number;
  maxImg: boolean;

  constructor(private gameService: GameService, private router: Router) {
    this.buttonDisabled = true;
    this.gameService.score$.subscribe(score => this.score = score);
    this.gameService.currentRound$.subscribe(round => this.currentRound = round);
    this.gameService.images$.subscribe(path => this.images = path);
    this.gameService.maxImg$.subscribe(bool => this.maxImg = bool);

    this.countImg = 1;
    this.gameService.getNextImage().then(data => this.buttonDisabled = false);
  }

  ngOnInit(): void {
  }

  newImg(): void {
    this.gameService.getAdditionnalImage();
    this.countImg++;

    if (this.countImg >= 6) {
      this.maxImg = true;
    }
  }

  onSubmit(): void {
    if (this.yearGuess == null) { return; }
    this.buttonDisabled = true;
    this.gameService.getScore(this.yearGuess).then(guessResult => {
      this.gameService.score$.next(this.score + guessResult.score);
      if (guessResult.score < 1000) {
        Swal.fire({
          icon: 'error',
          title: 'Vous avez gagné : ' + guessResult.score + ' points',
          html: 'L\'image correspondait à l\'année ' + guessResult.actualYear,
          timer: 3000
        });
      } else {
        Swal.fire({
          icon: 'success',
          title: 'Bravo ! Vous avez gagné : ' + guessResult.score + ' points',
          html: 'Vous avez trouvé la bonne année ! (' + guessResult.actualYear + ')',
          timer: 3000
        });
      }
    });
    this.yearGuess = null;
    this.maxImg = false;
    this.countImg = 1;
    if (this.currentRound < 10) {
      this.gameService.currentRound$.next(this.currentRound + 1);
      this.gameService.getNextImage().then(data => this.buttonDisabled = false);
    } else {
      this.router.navigate(['./result/']);
    }
  }
}
