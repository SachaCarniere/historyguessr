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
        'guess', 'actualYear', 'score',
    ];

    public function __construct(int $guess, int $actualYear) {
        parent::__construct();
        $this->guess = $guess;
        $this->actualYear = $actualYear;
        $this->score = max(1000 - pow(abs($guess-$actualYear), 3), 0);
        /*$difference = abs($guess-$actualYear);
        if ($difference == 0) {
            $this->score = 1000;
        } else {
            $this->score = (int) ( 1000 / ( 1 + exp(-5 * ($difference - ))));
        }*/
    }
}
