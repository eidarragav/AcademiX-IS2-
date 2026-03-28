<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\CoursesController;

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});


//Autenticacion
Route::post("/register", [AuthController::class, 'register']);
Route::post("/login", [AuthController::class, 'login']);
Route::post("/logout", [AuthController::class, 'logout'])->middleware('auth:sanctum');
Route::post("/restore_password", [AuthController::class, 'restore_password']);


//Courses routes
Route::post("/courses", [CoursesController::class, 'create_course'])->middleware('auth:sanctum');
Route::get("/courses", [CoursesController::class, 'index_courses']);
Route::get("/courses/{id}", [CoursesController::class, 'index_course']);
Route::put("/courses/{id}", [CoursesController::class, 'update_course']);
Route::delete("/courses/{id}", [CoursesController::class, 'delete_course']);
