import {Component, Input, OnInit} from '@angular/core';
import {GameService} from '../../services/game.service';
import {Router} from '@angular/router';
import Swal from 'sweetalert2';
import {NgbActiveModal, NgbModal} from '@ng-bootstrap/ng-bootstrap';

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

  constructor(private gameService: GameService, private router: Router, private modalSerive: NgbModal) {
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
    this.gameService.getAdditionnalImage().then(r => this.countImg++);

    if (this.countImg >= 6) {
      this.maxImg = true;
    }
  }

  onSubmit(): void {
    if (this.yearGuess == null || isNaN(this.yearGuess)) { return; }
    this.buttonDisabled = true;
    this.gameService.getScore(this.yearGuess).then(guessResult => {
      this.gameService.score$.next(this.score + guessResult.score);
      let imageHTMLCode = '';
      for (let i = 0; i < guessResult.images.length; i++){
        imageHTMLCode += '<div class="text-center">' +
                         '<img src="' + guessResult.images[i] + '" alt="' + guessResult.eventNames[i] + '" class="img-fluid zoom">' +
                         '<p>' + guessResult.eventNames[i] + '</p>' +
                         '<p>' + guessResult.captions[i] + '</p>' +
                         '</div>';
      }

      if (guessResult.actualYear !== guessResult.guess) {
        Swal.fire({
          icon: 'error',
          title: 'Vous avez gagné : ' + guessResult.score + ' points',
          html: '<p>L\'image correspondait à l\'année ' + guessResult.actualYear + '</p>' + imageHTMLCode
        });
      } else {
        Swal.fire({
          icon: 'success',
          title: 'Bravo ! Vous avez gagné : ' + guessResult.score + ' points',
          html: '<p>Vous avez trouvé la bonne année ! (' + guessResult.actualYear + ')</p>' + imageHTMLCode
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

  openModal(image): void{
    const modalRef = this.modalSerive.open(ImageModalComponent, { size: 'l' });
    modalRef.componentInstance.image = image;
  }
}

@Component({
  selector: 'app-image-modal',
  template: '<img src="{{image}}" alt="HistoryGuessrImage" class="img-fluid">',
  styles: ['img {width: 100%; height: auto;}']
})
export class ImageModalComponent {
  @Input() image;

  constructor(private activeModal: NgbActiveModal) {}
}
