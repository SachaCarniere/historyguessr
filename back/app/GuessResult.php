<?php


namespace App;

use Illuminate\Database\Eloquent\Model;

class GuessResult extends Model
{
    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'guess', 'actualYear', 'score', 'images', 'event_names', 'captions'
    ];

    public function __construct(int $guess, int $actualYear, int $roundId, int $amountUnlocked) {
        parent::__construct();
        $this->guess = $guess;
        $this->actualYear = $actualYear;
        # $this->score = max(1000 - pow(abs($guess-$actualYear), 3), 0);
        $difference = abs($guess-$actualYear);
        if ($difference == 0) {
            $this->score = 1000;
        } else {
            $this->score = (int) ( 1000 / ( 1 + exp(($difference/5 - 2))));
        }
        $round = Round::find($roundId);
        $images = $round->images()->get()->take($amountUnlocked);

        $this->images = collect();
        $this->event_names = collect();
        $this->captions = collect();
        //dd($images);
        foreach ($images as $key => $image){
            $this->images->push(env('APP_URL')."storage/img/".$image->path);
            $this->event_names->push($image->event_name);
            $this->captions->push($image->img_caption);
        }


    }
}
