<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class SubmissionsController extends Controller
{
    public function index_submission($id){

    }

    public function index_submissions(){
        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->get(env("SUBMISSIONS_EVALUATIONS_ENDPOINT"));

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ];
    }

    public function create_submission(Request $request){

    }

    public function update_submission(Request $request, $id){

    }

    public function delete_submission($id){

    }


}
