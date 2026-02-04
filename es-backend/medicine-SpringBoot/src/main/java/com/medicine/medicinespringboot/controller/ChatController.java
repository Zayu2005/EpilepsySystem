package com.medicine.medicinespringboot.controller;


import com.medicine.medicinespringboot.utils.AiChatTools;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.MessageChatMemoryAdvisor;
import org.springframework.ai.chat.memory.ChatMemory;
import org.springframework.ai.chat.memory.InMemoryChatMemory;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.ai.zhipuai.ZhiPuAiChatModel;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import com.medicine.medicinespringboot.utils.AiChatTools;

@CrossOrigin
@RestController
@RequestMapping ("/chat")
public class ChatController {


    @Autowired
    private ZhiPuAiChatModel zhiPuAiChatModel;
    @Autowired
    private AiChatController aiChatController;

    private final ChatMemory chatMemory = new InMemoryChatMemory();

    @GetMapping("/ai/generate")
    public String chat(@RequestParam String prompt) {
        ChatClient chatClient = ChatClient
                .builder(zhiPuAiChatModel)
                .build();
        return chatClient.prompt()
                .user(prompt)
                .call()
                .content();
    }

    @GetMapping(value = "/chat/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<String> streamChat(@RequestParam String prompt) {
        ChatClient chatClient = ChatClient
                .builder(zhiPuAiChatModel)
                .build();
        return chatClient.prompt()
                .user(prompt)
                .stream()
                .content();
    }

    @GetMapping(value = "/patient", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<String> chatStreamWithHistory(@RequestParam String prompt, @RequestParam(required = false) String sessionId) {
        System.out.println("sessionId:"+sessionId);
        MessageChatMemoryAdvisor advisor = new MessageChatMemoryAdvisor(chatMemory, sessionId, 100);
        ChatClient chatClient = ChatClient
                .builder(zhiPuAiChatModel).defaultSystem("""
                        你是一名专业的数字化癫痫医生,你需要辅助医生进行癫痫诊断和治疗，请以友好、乐于助人且愉快的方式进行回复，请你对
                        医生提出的问题进行回复""")
                .build();
        return chatClient
                .prompt("接下来会给你一个病人的信息，你需要给出病人的分析结果和建议,你面向的使用者是医生,所有的问题及回答都是向医生做出的")
                .tools(aiChatController)
                .user(prompt)
                .advisors(advisor)
                .stream()
                .content();
    }

}


