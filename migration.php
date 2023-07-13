<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint; 

class CreateWritingsTable extends Migration
{

  public function up()
  {
    
    // Raw SQL 
    $sql = "CREATE TABLE writings...";
    
    Schema::create('writings', function (Blueprint $table) {
        $table->id();
        $table->integer('source_id');
        $table->string('title')->nullable();
        $table->text('body');
        $table->integer('page_num');
        $table->date('created_date')->nullable();
        $table->timestamps();
    });

  }

}
