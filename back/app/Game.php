<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Game extends Model
{
    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'uuid'
    ];

    public function rounds()
    {
        return $this->hasMany('App\Round')->orderBy('index');
    }
}
