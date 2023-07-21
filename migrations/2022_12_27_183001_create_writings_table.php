<?php 

// 2022_12_27_183001_create_writings_table.php  

class CreateWritingsTable extends Migration  
{
  public function up()
  {
    Schema::create('writings', function (Blueprint $table) {
      $table->id();
      $table->integer('source_id');
      $table->string('title')->nullable();
      $table->text('body');
      $table->integer('page_num')->nullable();
      $table->date('created_date')->nullable();
      $table->timestamps();
    });
  }
}
