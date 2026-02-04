package com.medicine.medicinespringboot.interceptors;

import com.medicine.medicinespringboot.utils.JwtUtil;
import com.medicine.medicinespringboot.utils.ThreadLocalUtil;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import java.util.Map;

//拦截器实现登录拦截，
@Slf4j
@Component
public class LoginInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String token = request.getHeader("Authorization");
        log.info("拦截到请求");
        try {
            Map<String, Object> claims = JwtUtil.parseToken(token);
//            //把业务数据存储到ThreadLocal中
            ThreadLocalUtil.set(claims);
            log.info("解析成功，放行");
            return true;
        }catch (Exception e){
            response.setStatus(401);
            log.info("解析失败，拦截");
            return false;
        }
//        Map<String, Object> claims = JwtUtil.parseToken(token);
//        if (claims == null){
//            response.setStatus(401);
//            return false;
//        }
//        ThreadLocalUtil.set(claims);
//        return true;
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        ThreadLocalUtil.remove(); //请求结束，清除ThreadLocal
    }
}
