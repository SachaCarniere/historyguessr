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

  constructor(private gameService: GameService, private router: Router, private modalSerive: NgbModal) {
    this.buttonDisabled = true;
    this.gameService.score$.subscribe(score => this.score = score);
    this.gameService.currentRound$.subscribe(round => this.currentRound = round);
    this.gameService.images$.subscribe(path => this.images = path);
    this.gameService.getNextImage().then(data => this.buttonDisabled = false);
  }

  ngOnInit(): void {
  }

  newImg(): void {
    this.gameService.getAdditionnalImage();
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
    if (this.currentRound < 10) {
      this.gameService.currentRound$.next(this.currentRound + 1);
      this.gameService.getNextImage().then(data => this.buttonDisabled = false);
    } else {
      this.router.navigate(['./result/']);
    }
  }

  openModal(image): void{
    const modalRef = this.modalSerive.open(ImageModalComponent, { size: 'xl' });
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
