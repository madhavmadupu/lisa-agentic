"use client";

import { ModeToggle } from "@/components/mode-toggle";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Bot, Code2, FileText, Send, Terminal, User, RefreshCw } from "lucide-react";
import { useState, useRef, useEffect } from "react";
import { startAgentRun, API_BASE_URL, getWorkspaceFiles, getFileContent, getChatHistory, getSessions, Session, ChatMessage } from "@/lib/api";
import { EventSourcePolyfill } from "event-source-polyfill";
import { FileTree } from "@/components/file-tree";



export default function Home() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [terminalOutput, setTerminalOutput] = useState<string[]>([]);
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  // Workspace State
  const [files, setFiles] = useState<string[]>([]);
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [fileContent, setFileContent] = useState<string>("");

  // Session State
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);
  const [sessions, setSessions] = useState<Session[]>([]);

  const fetchFiles = async () => {
    try {
      const { files } = await getWorkspaceFiles();
      setFiles(files);
    } catch (err) {
      console.error("Failed to fetch files", err);
    }
  };

  const loadHistory = async (sessionId: string) => {
    try {
      const history = await getChatHistory(sessionId);
      setMessages(history);
      setCurrentSessionId(sessionId);
      setTerminalOutput(["> Loaded history for session: " + sessionId]);
    } catch (err) {
      console.error("Failed to load history", err);
    }
  };

  const loadSessions = async () => {
    try {
      const all = await getSessions();
      setSessions(all);
      if (all.length > 0 && !currentSessionId) {
        loadHistory(all[0].id);
      }
    } catch (err) {
      console.error("Failed to load sessions", err);
    }
  };

  useEffect(() => {
    fetchFiles();
    loadSessions();
  }, []);

  const handleFileSelect = async (path: string) => {
    setSelectedFile(path);
    try {
      const { content } = await getFileContent(path);
      setFileContent(content);
    } catch (err) {
      console.error(err);
      setFileContent("Error reading file.");
    }
  };

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const appendTerminal = (text: string) => {
    setTerminalOutput((prev) => [...prev, text]);
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async () => {
    if (!input.trim() || isProcessing) return;

    const userMsg = input;
    setInput("");

    // Optimistic update
    const optimisticMsg: ChatMessage = {
      id: Date.now(),
      session_id: currentSessionId || "temp",
      role: "user",
      content: userMsg,
      created_at: new Date().toISOString()
    };
    setMessages((prev) => [...prev, optimisticMsg]);

    setIsProcessing(true);
    appendTerminal(`> Starting task: ${userMsg}`);

    try {
      const { session_id } = await startAgentRun({ user_request: userMsg });
      appendTerminal(`> Session started: ${session_id}`);
      setCurrentSessionId(session_id);
      loadSessions();

      const eventSource = new EventSourcePolyfill(
        `${API_BASE_URL}/api/agent/stream/${session_id}`
      );

      eventSource.onmessage = (event: MessageEvent) => {
        const payload = JSON.parse(event.data);
        const { node, status, message } = payload;

        if (status === "complete") {
          appendTerminal("> Workflow completed.");
          // Refresh history to get the complete and correct DB state
          loadHistory(session_id);
          fetchFiles();
          eventSource.close();
          setIsProcessing(false);
          return;
        }

        if (status === "error") {
          appendTerminal(`> Error: ${message}`);
          eventSource.close();
          setIsProcessing(false);
          return;
        }

        if (node) {
          appendTerminal(`> Agent [${node}] active...`);
          if (node === "architect" && payload.plan) {
            // Optional: could show a temporary plan notification if desired
          }
        }
      };

      eventSource.onerror = (err: unknown) => {
        console.error("EventSource error:", err);
        eventSource.close();
        setIsProcessing(false);
      };

    } catch (error) {
      console.error(error);
      setIsProcessing(false);
    }
  };

  return (
    <div className="flex h-screen w-full flex-col bg-background md:flex-row">
      {/* Sidebar */}
      <aside className="w-full border-r bg-muted/40 md:w-[300px] md:flex-col lg:w-[350px]">
        <div className="flex h-14 items-center border-b px-4 lg:h-[60px]">
          <div className="flex items-center gap-2 font-semibold">
            <Bot className="h-6 w-6" />
            <span>LISA Agentic</span>
          </div>
          <div className="ml-auto">
            <ModeToggle />
          </div>
        </div>
        <div className="flex-1 overflow-auto py-4">
          <ScrollArea className="h-full px-4">
            <div className="space-y-4">
              <div>
                <h3 className="mb-2 px-2 text-sm font-semibold tracking-tight">Sessions</h3>
                <div className="space-y-1">
                  <Button variant="outline" className="w-full justify-start mb-2" onClick={() => {
                    setCurrentSessionId(null);
                    setMessages([]);
                    setTerminalOutput([]);
                  }}>
                    <FileText className="mr-2 h-4 w-4" />
                    New Session
                  </Button>
                  {sessions.map((session) => (
                    <Button
                      key={session.id}
                      variant={currentSessionId === session.id ? "secondary" : "ghost"}
                      className="w-full justify-start text-xs truncate"
                      onClick={() => loadHistory(session.id)}
                    >
                      <span className="truncate">{session.title || "Untitled Session"}</span>
                    </Button>
                  ))}
                </div>
              </div>

              <Separator />

              {/* File Tree Integration */}
              <div>
                <div className="flex items-center justify-between px-2 mb-2">
                  <h3 className="text-sm font-semibold tracking-tight">Workspace</h3>
                  <Button variant="ghost" size="icon" className="h-6 w-6" onClick={fetchFiles}>
                    <RefreshCw className="h-3 w-3" />
                  </Button>
                </div>
                <div className="border rounded-md bg-background h-[300px]">
                  <FileTree files={files} onSelect={handleFileSelect} />
                </div>
              </div>
            </div>
          </ScrollArea>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex flex-1 flex-col overflow-hidden">
        {/* Header/Status Bar */}
        <header className="flex h-14 items-center gap-4 border-b bg-muted/40 px-6 lg:h-[60px]">
          <span className="font-semibold">Current Task: {isProcessing ? "Running..." : "Idle"}</span>
          <div className="ml-auto flex items-center gap-2">
            <span className="text-xs text-muted-foreground">Agents: {isProcessing ? "Active" : "Idle"}</span>
          </div>
        </header>

        {/* Content Area */}
        <div className="flex flex-1 overflow-hidden">
          {/* Chat/Interaction Panel */}
          <div className="flex w-1/2 flex-col border-r">
            <ScrollArea className="flex-1 p-4" ref={scrollAreaRef}>
              <div className="space-y-4">
                {messages.map((msg, i) => (
                  <div key={i} className="flex gap-3">
                    <div
                      className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full ${msg.role === "agent"
                        ? "bg-primary text-primary-foreground"
                        : "bg-primary/10"
                        }`}
                    >
                      {msg.role === "agent" ? <Bot className="h-4 w-4" /> : <User className="h-4 w-4" />}
                    </div>
                    <div
                      className={`${msg.role === "agent" ? "bg-primary/10" : "bg-muted"
                        } p-3 rounded-lg text-sm max-w-[80%] whitespace-pre-wrap font-mono`}
                    >
                      {msg.content}
                    </div>
                  </div>
                ))}
                <div ref={messagesEndRef} />
              </div>
            </ScrollArea>
            <div className="p-4 border-t">
              <div className="relative">
                <Input
                  placeholder="Describe your task..."
                  className="pr-12"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
                  disabled={isProcessing}
                />
                <Button
                  size="icon"
                  className="absolute right-1 top-1 h-8 w-8"
                  variant="ghost"
                  onClick={handleSubmit}
                  disabled={isProcessing}
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>

          {/* Workspace/Artifacts Panel */}
          <div className="flex flex-1 flex-col bg-muted/10">
            <Tabs defaultValue="code" className="flex-1 flex flex-col">
              <div className="flex items-center justify-between px-4 py-2 border-b">
                <TabsList>
                  <TabsTrigger value="code" className="flex items-center gap-2">
                    <Code2 className="h-4 w-4" /> Code
                  </TabsTrigger>
                  <TabsTrigger value="terminal" className="flex items-center gap-2">
                    <Terminal className="h-4 w-4" /> Terminal
                  </TabsTrigger>
                </TabsList>
              </div>

              <div className="flex-1 overflow-hidden p-4">
                <TabsContent value="code" className="h-full m-0">
                  <Card className="h-full flex flex-col border-0 shadow-none">
                    <CardHeader className="p-4 border-b flex flex-row items-center justify-between space-y-0">
                      <CardTitle className="text-sm font-mono truncate max-w-[calc(100%-24px)]">
                        {selectedFile || "Select a file"}
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="flex-1 p-0 overflow-hidden font-mono text-sm">
                      <ScrollArea className="h-full p-4">
                        {selectedFile ? (
                          <pre className="text-muted-foreground whitespace-pre-wrap">{fileContent}</pre>
                        ) : (
                          <div className="flex items-center justify-center h-full text-muted-foreground">
                            Select a file from the workspace to view content.
                          </div>
                        )}
                      </ScrollArea>
                    </CardContent>
                  </Card>
                </TabsContent>

                <TabsContent value="terminal" className="h-full m-0">
                  <Card className="h-full flex flex-col border-0 shadow-none bg-black text-white">
                    <CardContent className="flex-1 p-4 font-mono text-xs overflow-auto">
                      {terminalOutput.map((line, i) => (
                        <div key={i}>{line}</div>
                      ))}
                    </CardContent>
                  </Card>
                </TabsContent>
              </div>
            </Tabs>
          </div>
        </div>
      </main>
    </div>
  );
}
