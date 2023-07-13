<?php

namespace App\Jobs;

use App\Services\TextImporter;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldBeUnique;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

class ProcessTextsJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    /**
     * Execute the job.
     *
     * @param  \App\Services\TextImporter  $importer
     * @return void
     */
    public function handle(TextImporter $importer)
    {
        $importer->import();
        
        // Log progress updates
        $this->progress(50); 
        
        // Handle failures
        if ($importer->hasFailed()) {
            $this->failed($importer->getLastError());
        }
    }
}
