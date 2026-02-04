package com.medicine.medicinespringboot.controller;


import com.medicine.medicinespringboot.pojo.PageBean;
import com.medicine.medicinespringboot.pojo.Result;
import com.medicine.medicinespringboot.pojo.Todo;
import com.medicine.medicinespringboot.pojo.User;
import com.medicine.medicinespringboot.service.Impl.TodoService;
import com.medicine.medicinespringboot.service.Impl.UserService;
import com.medicine.medicinespringboot.utils.ThreadLocalUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/todo")
public class TodoController {


    @Autowired
    private TodoService todoService;
    @Autowired
    private UserService userService;

    @PostMapping("add")
    public Result addTodo(@RequestBody Todo todo) {
        Map<String, Object> map = ThreadLocalUtil.get();
        String username = (String) map.get("username");
        User user = userService.findByUsername(username);   //查询这个用户
        todo.setUserId(Integer.valueOf(user.getId()));
        todoService.add(todo);
        log.info("用户{},添加了待办事项,todo:{}", username, todo);
        return Result.success();
    }

    //获得待办的列表
    @GetMapping("/list")
    public Result<PageBean<Todo>> list(
            @RequestParam(required = true) Integer pageNum,
            @RequestParam(required = true) Integer pageSize,
            @RequestParam(required = false) Integer completed
    ) {
        Map<String, Object> map = ThreadLocalUtil.get();
        String username = (String) map.get("username");
        User user = userService.findByUsername(username);
        Integer userId = Integer.valueOf(user.getId());
        log.info("用户{},进行Todo多页查询,pageNum:{},pageSize{}", username, pageNum, pageSize);
        PageBean<Todo> pageBean = todoService.list(pageNum, pageSize, completed, userId);
        return Result.success(pageBean);
    }
    //删除指定id待办
    @DeleteMapping("/delete/{id}")
    public Result delete(@PathVariable Integer id){
        Map<String, Object> map = ThreadLocalUtil.get();
        //获得用户名、用户id
        String username = (String) map.get("username");
        User user = userService.findByUsername(username);
        Integer userId = Integer.valueOf(user.getId());
        //获得创建Todo用户的id
        Todo todo = todoService.findTodoById(id);
        Integer createTodoUserId = todo.getUserId();
        if(userId.equals(createTodoUserId)) {
            todoService.delete(id);
            log.info("用户{},删除了待办事项,todo title:{}", username, todo.getContent());
            return Result.success("删除成功");
        }
        return Result.error("删除失败，请联系管理员");
    }
    //更新指定id代办的状态
    @PutMapping("status")
    public Result update(@RequestParam Integer id){
        Map<String, Object> map = ThreadLocalUtil.get();
        String username = (String) map.get("username");
        User user = userService.findByUsername(username);
        Integer userId = Integer.valueOf(user.getId());
        Todo todo = todoService.findTodoById(id);
        if(todo.getUserId().equals(userId)){
            Boolean completed = todo.getCompleted();
            todo.setCompleted(!completed);
            todoService.update(todo);
        }else{
            return Result.error("非创建人员,无法修改状态");
        }
        return Result.success();
    }
}
