<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Round extends Model
{
    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'index', 'year_answered','amount_unlocked'
    ];

    /**
     * The attributes that should be hidden for arrays.
     *
     * @var array
     */
    protected $hidden = [
        'year'
    ];

    public function game()
    {
        return $this->belongsTo('App\Game');
    }

    public function images()
    {
        return $this->belongsToMany('App\Image');
    }
}
