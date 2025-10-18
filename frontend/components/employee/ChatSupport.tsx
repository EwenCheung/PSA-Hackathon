import { useEffect, useRef, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Textarea } from '../ui/textarea';
import { Badge } from '../ui/badge';
import { Alert, AlertDescription } from '../ui/alert';
import {
  Send,
  Heart,
  AlertCircle,
  Shield,
  Smile,
  Meh,
  Frown,
  MessageCircle,
  Loader2,
} from 'lucide-react';
import {
  fetchWellbeingMessages,
  sendWellbeingMessage,
  WellbeingMessage,
} from '../../src/services/wellbeing';

interface Message {
  id: string;
  sender: 'user' | 'ai';
  content: string;
  timestamp: Date;
  isAnonymous: boolean;
  anonSessionId?: string | null;
}

interface ChatSupportProps {
  employeeId: string;
}

const INITIAL_GREETING: Message = {
  id: 'greeting',
  sender: 'ai',
  content: "Hello! I'm here to support your wellbeing. How are you feeling today? This is a safe, confidential space.",
  timestamp: new Date(),
  isAnonymous: false,
};

export default function ChatSupport({ employeeId }: ChatSupportProps) {
  const [messages, setMessages] = useState<Message[]>([INITIAL_GREETING]);
  const [input, setInput] = useState('');
  const [sentiment, setSentiment] = useState<'positive' | 'neutral' | 'negative'>('neutral');
  const [isAnonymousMode, setIsAnonymousMode] = useState(false);
  const [anonSessionId, setAnonSessionId] = useState<string | null>(null);
  const [isLoadingHistory, setIsLoadingHistory] = useState(true);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let active = true;
    const loadHistory = async () => {
      setIsLoadingHistory(true);
      try {
        const history = await fetchWellbeingMessages(employeeId);
        if (!active) return;
        if (history.length === 0) {
          setMessages([INITIAL_GREETING]);
          return;
        }
        const mapped = history.map(mapToClientMessage);
        setMessages(mapped);

        const latestAnon = [...mapped]
          .reverse()
          .find((message) => message.isAnonymous && message.anonSessionId);
        if (latestAnon) {
          setAnonSessionId(latestAnon.anonSessionId ?? null);
        }
      } catch (loadError) {
        if (active) {
          setError('We could not load your previous wellbeing messages.');
          setMessages([INITIAL_GREETING]);
        }
      } finally {
        if (active) {
          setIsLoadingHistory(false);
        }
      }
    };

    loadHistory();

    return () => {
      active = false;
    };
  }, [employeeId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (isAnonymousMode) {
      setAnonSessionId(null);
    }
  }, [isAnonymousMode]);

  const analyzeSentiment = (text: string): 'positive' | 'neutral' | 'negative' => {
    const lowerText = text.toLowerCase();
    const negativeWords = ['sad', 'depressed', 'anxious', 'stressed', 'worried', 'tired', 'overwhelmed', 'difficult', 'hard', 'struggle', 'pain', 'hurt', 'alone', 'isolated'];
    const positiveWords = ['happy', 'good', 'great', 'excellent', 'excited', 'motivated', 'confident', 'grateful', 'better', 'wonderful'];

    let score = 0;
    negativeWords.forEach((word) => {
      if (lowerText.includes(word)) score -= 1;
    });
    positiveWords.forEach((word) => {
      if (lowerText.includes(word)) score += 1;
    });

    if (score < -1) return 'negative';
    if (score > 1) return 'positive';
    return 'neutral';
  };

  const handleSend = async () => {
    const trimmed = input.trim();
    if (!trimmed || isSending) return;

    setInput('');
    setError(null);
    setIsSending(true);

    const nextSentiment = analyzeSentiment(trimmed);
    setSentiment(nextSentiment);

    const timestamp = new Date();
    const userMessage: Message = {
      id: `user-${timestamp.getTime()}`,
      sender: 'user',
      content: trimmed,
      timestamp,
      isAnonymous: isAnonymousMode,
      anonSessionId: isAnonymousMode ? anonSessionId : null,
    };

    const aiMessageId = `ai-${timestamp.getTime()}`;
    const placeholderMessage: Message = {
      id: aiMessageId,
      sender: 'ai',
      content: '',
      timestamp,
      isAnonymous: isAnonymousMode,
      anonSessionId: isAnonymousMode ? anonSessionId : null,
    };

    setMessages((prev) => [...prev, userMessage, placeholderMessage]);

    const updateMessage = (id: string, updater: (message: Message) => Message) => {
      setMessages((prev) => prev.map((message) => (message.id === id ? updater(message) : message)));
    };

    try {
      const response = await sendWellbeingMessage(
        employeeId,
        trimmed,
        {
          isAnonymous: isAnonymousMode,
          anonSessionId: isAnonymousMode ? anonSessionId : null,
        },
      );
      const finalMessage = mapToClientMessage(response);
      updateMessage(aiMessageId, () => finalMessage);
      if (isAnonymousMode && finalMessage.anonSessionId) {
        setAnonSessionId(finalMessage.anonSessionId);
      }
      if (finalMessage.content === 'Message failed to send, please try again.') {
        setError('Message failed to send, please try again.');
      }
    } catch (sendError) {
      updateMessage(aiMessageId, (message) => ({
        ...message,
        content: 'Message failed to send, please try again.',
      }));
      setError('Message failed to send, please try again.');
    } finally {
      setIsSending(false);
    }
  };

  const getSentimentIcon = () => {
    switch (sentiment) {
      case 'positive':
        return <Smile className="w-5 h-5 text-green-600" />;
      case 'negative':
        return <Frown className="w-5 h-5 text-destructive" />;
      default:
        return <Meh className="w-5 h-5 text-muted-foreground" />;
    }
  };

  const getSentimentText = () => {
    switch (sentiment) {
      case 'positive':
        return 'Positive mood detected';
      case 'negative':
        return 'You seem to be struggling';
      default:
        return 'Neutral mood';
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-4">
      <Card className="border border-[#D0E8F5]">
        <CardHeader className="border-b border-[#E8F3F9]">
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Heart className="w-5 h-5 text-[#4167B1]" />
                Wellbeing Support Chat
              </CardTitle>
              <CardDescription>
                A safe space for you to express yourself and get support
              </CardDescription>
            </div>
            <div className="flex items-center gap-2">
              {getSentimentIcon()}
              <span className="text-sm">{getSentimentText()}</span>
            </div>
          </div>
        </CardHeader>
      </Card>

      {isAnonymousMode && (
        <Alert className="border-[#4167B1]/20 bg-[#DEF0F9]">
          <Shield className="w-4 h-4 text-[#4167B1]" />
          <AlertDescription>
            <div className="flex items-center justify-between">
              <span>
                <strong>Anonymous Mode Active:</strong> Your identity is completely hidden.
                Feel free to speak openly.
              </span>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsAnonymousMode(false)}
              >
                Exit
              </Button>
            </div>
          </AlertDescription>
        </Alert>
      )}

      {!isAnonymousMode && sentiment === 'negative' && (
        <Alert className="border-secondary/20 bg-orange-50">
          <AlertCircle className="w-4 h-4 text-secondary" />
          <AlertDescription>
            <div className="flex items-center justify-between">
              <span>
                Need to speak freely? Enable anonymous mode for complete privacy.
              </span>
              <Button
                size="sm"
                onClick={() => setIsAnonymousMode(true)}
              >
                Enable Anonymous Mode
              </Button>
            </div>
          </AlertDescription>
        </Alert>
      )}

      {error && (
        <Alert className="border-destructive/20 bg-red-50">
          <AlertCircle className="w-4 h-4 text-destructive" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <Card className="h-[500px] flex flex-col border border-[#D0E8F5]">
        <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
          {isLoadingHistory && (
            <div className="text-sm text-muted-foreground">Loading your conversation...</div>
          )}
          {!isLoadingHistory &&
            messages.map((message) => (
              <div
                key={`${message.id}-${message.timestamp.getTime()}`}
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[70%] rounded-lg p-4 ${
                    message.sender === 'user'
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-muted text-foreground'
                  }`}
                >
                  {message.isAnonymous && (
                    <Badge variant="secondary" className="mb-2">
                      <Shield className="w-3 h-3 mr-1" />
                      Anonymous
                    </Badge>
                  )}
                  <p className="whitespace-pre-wrap">{message.content}</p>
                  <p
                    className={`text-xs mt-2 ${
                      message.sender === 'user' ? 'text-primary-foreground/70' : 'text-muted-foreground'
                    }`}
                  >
                    {message.timestamp.toLocaleTimeString()}
                  </p>
                </div>
              </div>
            ))}
          <div ref={messagesEndRef} />
        </CardContent>

        <div className="border-t p-4">
          <div className="flex gap-2">
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              placeholder={isAnonymousMode ? 'Speak freely... (Anonymous)' : "Share how you're feeling..."}
              className="min-h-[80px] resize-none"
            />
            <Button onClick={handleSend} className="self-end" disabled={isSending}>
              {isSending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
            </Button>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            Press Enter to send, Shift+Enter for new line. All conversations are confidential.
          </p>
        </div>
      </Card>

      <Card className="border border-[#D0E8F5]">
        <CardHeader className="border-b border-[#E8F3F9]">
          <CardTitle className="text-base">Additional Support Resources</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <div className="flex items-center gap-2 text-sm">
            <MessageCircle className="w-4 h-4 text-[#4167B1]" />
            <span>HR Support: hr@company.com</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <Heart className="w-4 h-4 text-red-600" />
            <span>Employee Assistance Program: 1-800-XXX-XXXX</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <AlertCircle className="w-4 h-4 text-yellow-600" />
            <span>Crisis Support: Available 24/7</span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

const mapToClientMessage = (message: WellbeingMessage): Message => ({
  id: `${message.sender}-${message.timestamp}`,
  sender: message.sender,
  content: message.content,
  timestamp: new Date(message.timestamp),
  isAnonymous: message.isAnonymous,
  anonSessionId: message.anonSessionId,
});
