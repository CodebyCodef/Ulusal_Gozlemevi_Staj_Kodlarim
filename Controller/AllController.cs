using Microsoft.AspNetCore.Mvc;

using APIforUsers.UserModel;



namespace APIforUsers
{
	[ApiController]
	[Route("api/[controller]")]

	public class RegisterController : ControllerBase
	{
		[HttpPost]

		public IActionResult Register(UserInfo newUser)
		{
			newUser.Id = newUser.Id;
			newUser.Email = newUser.Email.ToLower();
			newUser.Password = newUser.Password.ToLower();


			return Ok("Yeni Kayýt Baþarýlý");
		}

	}



	public class ShowController : ControllerBase
	{
		[HttpGet]
		public IActionResult Show()
		{
			return Ok("Kayýtlý Kullanýcýlar Gösteriliyor");
		}
	}

}