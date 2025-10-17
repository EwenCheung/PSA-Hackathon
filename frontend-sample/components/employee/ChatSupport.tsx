import { useState, useRef, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Textarea } from '../ui/textarea';
import { Badge } from '../ui/badge';
import { Alert, AlertDescription } from '../ui/alert';
import { 
  Send, Heart, AlertCircle, Shield, 
  Smile, Meh, Frown, MessageCircle 
} from 'lucide-react';

interface Message {
  id: number;
  sender: 'user' | 'ai';
  content: string;
  timestamp: Date;
  isAnonymous?: boolean;
}

interface ChatSupportProps {
  employeeId: string;
}

export default function ChatSupport({ employeeId }: ChatSupportProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      sender: 'ai',
      content: "Hello! I'm here to support your wellbeing. How are you feeling today? This is a safe, confidential space.",
      timestamp: new Date(),
    }
  ]);
  const [input, setInput] = useState('');
  const [sentiment, setSentiment] = useState<'positive' | 'neutral' | 'negative'>('neutral');
  const [isAnonymousMode, setIsAnonymousMode] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Simple sentiment analysis
  const analyzeSentiment = (text: string): 'positive' | 'neutral' | 'negative' => {
    const lowerText = text.toLowerCase();
    const negativeWords = ['sad', 'depressed', 'anxious', 'stressed', 'worried', 'tired', 'overwhelmed', 'difficult', 'hard', 'struggle', 'pain', 'hurt', 'alone', 'isolated'];
    const positiveWords = ['happy', 'good', 'great', 'excellent', 'excited', 'motivated', 'confident', 'grateful', 'better', 'wonderful'];
    
    let score = 0;
    negativeWords.forEach(word => {
      if (lowerText.includes(word)) score -= 1;
    });
    positiveWords.forEach(word => {
      if (lowerText.includes(word)) score += 1;
    });

    if (score < -1) return 'negative';
    if (score > 1) return 'positive';
    return 'neutral';
  };

  const getAIResponse = (userMessage: string, detectedSentiment: 'positive' | 'neutral' | 'negative'): string => {
    if (detectedSentiment === 'negative') {
      const responses = [
        "I hear that you're going through a difficult time. It's completely okay to feel this way. Would you like to talk more about what's been bothering you?",
        "Thank you for sharing that with me. It takes courage to express these feelings. Remember, you're not alone, and it's okay to ask for help.",
        "I can sense that things have been challenging for you. Your wellbeing matters. Would it help to discuss what's been weighing on your mind?",
        "I'm here to listen. Sometimes just expressing our feelings can help. What's been the most difficult part for you?",
      ];
      return responses[Math.floor(Math.random() * responses.length)];
    } else if (detectedSentiment === 'positive') {
      const responses = [
        "That's wonderful to hear! I'm glad things are going well. Keep up the positive momentum!",
        "It's great to see you in good spirits! What's been contributing to your positive outlook?",
        "I'm happy to hear that! Remember to celebrate these moments.",
      ];
      return responses[Math.floor(Math.random() * responses.length)];
    } else {
      const responses = [
        "Thank you for checking in. How can I support you today?",
        "I'm here to listen. Feel free to share whatever is on your mind.",
        "How has your week been going? I'm here if you need someone to talk to.",
      ];
      return responses[Math.floor(Math.random() * responses.length)];
    }
  };

  const handleSend = () => {
    if (!input.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: messages.length + 1,
      sender: 'user',
      content: input,
      timestamp: new Date(),
      isAnonymous: isAnonymousMode,
    };

    setMessages([...messages, userMessage]);

    // Analyze sentiment
    const detectedSentiment = analyzeSentiment(input);
    setSentiment(detectedSentiment);

    // Check if anonymous mode should be triggered
    if (detectedSentiment === 'negative' && !isAnonymousMode) {
      setTimeout(() => {
        const anonymousAlert: Message = {
          id: messages.length + 2,
          sender: 'ai',
          content: "I've noticed you might be going through a tough time. Would you like to enable anonymous mode? Your identity will be completely hidden, and you can speak freely.",
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, anonymousAlert]);
      }, 1000);
    }

    // Generate AI response
    setTimeout(() => {
      const aiMessage: Message = {
        id: messages.length + (detectedSentiment === 'negative' && !isAnonymousMode ? 3 : 2),
        sender: 'ai',
        content: getAIResponse(input, detectedSentiment),
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, aiMessage]);
    }, detectedSentiment === 'negative' && !isAnonymousMode ? 2000 : 1000);

    setInput('');
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
      {/* Header Card */}
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

      {/* Anonymous Mode Alert */}
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

      {/* Chat Area */}
      <Card className="h-[500px] flex flex-col border border-[#D0E8F5]">
        <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
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
                <p className={`text-xs mt-2 ${
                  message.sender === 'user' ? 'text-primary-foreground/70' : 'text-muted-foreground'
                }`}>
                  {message.timestamp.toLocaleTimeString()}
                </p>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </CardContent>

        {/* Input Area */}
        <div className="border-t p-4">
          <div className="flex gap-2">
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              placeholder={isAnonymousMode ? "Speak freely... (Anonymous)" : "Share how you're feeling..."}
              className="min-h-[80px] resize-none"
            />
            <Button onClick={handleSend} className="self-end">
              <Send className="w-4 h-4" />
            </Button>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            Press Enter to send, Shift+Enter for new line. All conversations are confidential.
          </p>
        </div>
      </Card>

      {/* Support Resources */}
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
