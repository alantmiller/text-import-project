<?php

// 2022_12_27_183000_create_sources_table.php

class CreateSourcesTable extends Migration
{
  public function up()
  {
    Schema::create('sources', function (Blueprint $table) {
      $table->id();
      $table->string('source');  
      $table->timestamps();
    });
    
    DB::table('sources')->insert([
      ['source' => 'Irmgard'],
      ['source' => 'Philipp'], 
      // etc
    ]);
  }
}
