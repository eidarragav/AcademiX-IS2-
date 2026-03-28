<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class CoursesController extends Controller
{
    public function create_course(Request $request){
        
    }

    public function index_courses(){
        $response = Http::withHeaders([
            "Authorization" => env("services_token")
        ])->get(env("courses_endpoint"));

        return [
            "status" => $response->status,
            "body" => $response->body
        ];
    }

    public function index_course($id){
        $response = Http::withHeaders([
            "Authorization" => env("services_token")
        ])->get(env("courses_endpoint")."/".$id);

        return [
            "status" => $response->status,
            "body" => $response->body
        ];
    }

    public function update_course(Request $request, $id){

    }

    public function delete_course(Request $request, $id){

    }
}
