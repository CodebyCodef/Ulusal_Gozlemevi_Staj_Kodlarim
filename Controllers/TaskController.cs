using Microsoft.AspNetCore.Mvc;

using denemeAPI.Models;


namespace denemeAPI.Controllers
{
    [ApiController]

    [Route("api/[controller]")]

    public class TasksController : ControllerBase
    {
        private static List<TaskItem> _tasks = new List<TaskItem>
        {
            new TaskItem {Id= 1, Title = "Ders Çalýþ", IsCompleted=false  },
            new TaskItem {Id= 2, Title = "Kitap Oku", IsCompleted=true  },

        };

        [HttpGet("{id}")]
        public IActionResult GetById(int id)
        {
            var task = _tasks.FirstOrDefault(x => x.Id == id);
            if (task == null)
            {
                return NotFound();
            }
            return Ok(task);
        }


        [HttpGet]
        public IActionResult GetAll()
        {
            return Ok(_tasks);
        }


        [HttpPost]
        public IActionResult Create(TaskItem newTask)
        {
            newTask.Id = _tasks.Max(x => x.Id) + 1;
            _tasks.Add(newTask);

            return CreatedAtAction(nameof(GetById), new{Id = newTask.Id},newTask);
        }

        [HttpPut("{id}")]
        public IActionResult Update(int id, TaskItem updatedTask)
        {
            var existingTask = _tasks.FirstOrDefault(task => task.Id == id);
            if (existingTask != null)
            {
                return NotFound();
            }

            existingTask.Title = updatedTask.Title;
            existingTask.IsCompleted = updatedTask.IsCompleted;

            return NoContent();
        }

        [HttpDelete("{id}")]
        public IActionResult Delete(int id) 
        {
            var task = _tasks.FirstOrDefault(t => t.Id == id);
            if (task == null)
            {
                return NotFound();

            
            }
            _tasks.Remove(task);

            return NoContent();
        }
    }
}