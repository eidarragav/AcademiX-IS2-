<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithFaker;
use Tests\TestCase;
use App\Models\User;
use Illuminate\Support\Facades\Hash;

class AuthTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_register()
    {
        $response = $this->postJson('/api/register', [
            'name' => 'Test',
            'email' => 'test@test.com',
            'password' => '123456',
            'question' => 'color?',
            'answer' => 'azul'
        ]);

        $response->assertStatus(200);

        $this->assertDatabaseHas('users', [
            'email' => 'test@test.com'
        ]);
    }

    public function test_user_can_login()
    {
        $user = User::factory()->create([
            'password' => Hash::make('123456')
        ]);

        $response = $this->postJson('/api/login', [
            'email' => $user->email,
            'password' => '123456'
        ]);

        $response->assertStatus(200)
                 ->assertJsonStructure(['access_token', 'token_type']);
    }

    public function test_login_fails_with_wrong_password()
    {
        $user = User::factory()->create([
            'password' => Hash::make('123456')
        ]);

        $response = $this->postJson('/api/login', [
            'email' => $user->email,
            'password' => 'wrongpass'
        ]);

        $response->assertStatus(200)
                 ->assertJson(['Acceso denegado' => 'Credenciales invalidades']);
    }

    public function test_restore_password_success()
    {
        $user = User::factory()->create([
            'answer' => 'azul',
            'password' => Hash::make('oldpass')
        ]);

        $response = $this->postJson('/api/restore_password', [
            'email' => $user->email,
            'answer' => 'azul',
            'password' => 'newpass'
        ]);

        $response->assertStatus(200);

        $this->assertTrue(
            Hash::check('newpass', $user->fresh()->password)
        );
    }

    public function test_restore_password_fails_with_wrong_answer()
    {
        $user = User::factory()->create([
            'answer' => 'azul'
        ]);

        $response = $this->postJson('/api/restore_password', [
            'email' => $user->email,
            'answer' => 'rojo',
            'password' => 'newpass'
        ]);

        $response->assertStatus(200)
                 ->assertJson(['message' => 'Respues incorrecta']);
    }
}
