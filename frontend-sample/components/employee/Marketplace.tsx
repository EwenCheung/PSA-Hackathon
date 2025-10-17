import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { 
  Gift, Coffee, Book, Ticket, 
  Smartphone, Award, ShoppingCart, CheckCircle2 
} from 'lucide-react';
import { Alert, AlertDescription } from '../ui/alert';

interface MarketplaceProps {
  points: number;
  onPointsUpdate: (points: number) => void;
}

const marketplaceItems = [
  {
    id: 1,
    name: 'Coffee Voucher',
    description: 'Enjoy a premium coffee on us',
    points: 50,
    icon: Coffee,
    category: 'Food & Drink',
    inStock: true,
  },
  {
    id: 2,
    name: 'Book of Your Choice',
    description: 'Select any book up to $30',
    points: 200,
    icon: Book,
    category: 'Learning',
    inStock: true,
  },
  {
    id: 3,
    name: 'Movie Tickets (2x)',
    description: 'Two tickets to any theater',
    points: 300,
    icon: Ticket,
    category: 'Entertainment',
    inStock: true,
  },
  {
    id: 4,
    name: 'Extra Day Off',
    description: 'One additional paid day off',
    points: 500,
    icon: Gift,
    category: 'Time Off',
    inStock: true,
  },
  {
    id: 5,
    name: 'Tech Gadget Voucher',
    description: '$100 towards tech accessories',
    points: 750,
    icon: Smartphone,
    category: 'Technology',
    inStock: true,
  },
  {
    id: 6,
    name: 'Professional Certification',
    description: 'Full coverage for one certification exam',
    points: 1000,
    icon: Award,
    category: 'Career',
    inStock: true,
  },
];

export default function Marketplace({ points, onPointsUpdate }: MarketplaceProps) {
  const [recentPurchase, setRecentPurchase] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('All');

  const categories = ['All', ...Array.from(new Set(marketplaceItems.map(item => item.category)))];

  const handleRedeem = (item: typeof marketplaceItems[0]) => {
    if (points >= item.points) {
      onPointsUpdate(points - item.points);
      setRecentPurchase(item.name);
      setTimeout(() => setRecentPurchase(null), 5000);
    }
  };

  const filteredItems = selectedCategory === 'All' 
    ? marketplaceItems 
    : marketplaceItems.filter(item => item.category === selectedCategory);

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <Card className="border border-[#D0E8F5]">
        <CardHeader className="border-b border-[#E8F3F9]">
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <ShoppingCart className="w-5 h-5 text-[#4167B1]" />
                Rewards Marketplace
              </CardTitle>
              <CardDescription>
                Redeem your earned points for exciting rewards
              </CardDescription>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-600">Available Points</p>
              <p className="text-3xl">{points}</p>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Recent Purchase Alert */}
      {recentPurchase && (
        <Alert className="border-green-500/20 bg-green-50">
          <CheckCircle2 className="w-4 h-4 text-green-600" />
          <AlertDescription>
            <strong>Success!</strong> You've redeemed {recentPurchase}. Check your email for details.
          </AlertDescription>
        </Alert>
      )}

      {/* Category Filter */}
      <div className="flex gap-2 flex-wrap">
        {categories.map(category => (
          <Button
            key={category}
            variant={selectedCategory === category ? 'default' : 'outline'}
            size="sm"
            onClick={() => setSelectedCategory(category)}
          >
            {category}
          </Button>
        ))}
      </div>

      {/* Items Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredItems.map((item) => {
          const Icon = item.icon;
          const canAfford = points >= item.points;

          return (
            <Card key={item.id} className={`border border-[#D0E8F5] ${!canAfford ? 'opacity-60' : ''}`}>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="w-12 h-12 bg-[#DEF0F9] rounded-lg flex items-center justify-center mb-3">
                    <Icon className="w-6 h-6 text-[#4167B1]" />
                  </div>
                  <Badge variant="secondary">{item.category}</Badge>
                </div>
                <CardTitle className="text-base">{item.name}</CardTitle>
                <CardDescription>{item.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Award className="w-5 h-5 text-yellow-600" />
                      <span className="text-xl">{item.points} pts</span>
                    </div>
                    {item.inStock && (
                      <Badge variant="outline" className="text-green-600">
                        In Stock
                      </Badge>
                    )}
                  </div>
                  
                  <Button 
                    className="w-full"
                    disabled={!canAfford || !item.inStock}
                    onClick={() => handleRedeem(item)}
                  >
                    {!canAfford ? `Need ${item.points - points} more pts` : 'Redeem Now'}
                  </Button>

                  {!canAfford && (
                    <p className="text-xs text-center text-gray-500">
                      Complete more courses or mentor others to earn points
                    </p>
                  )}
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* How to Earn Points */}
      <Card className="border border-[#D0E8F5]">
        <CardHeader className="border-b border-[#E8F3F9]">
          <CardTitle className="text-base">How to Earn More Points</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <span>Complete a course</span>
            <Badge variant="secondary">100-250 pts</Badge>
          </div>
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <span>Mentor a colleague</span>
            <Badge variant="secondary">50 pts/session</Badge>
          </div>
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <span>Receive mentor recognition</span>
            <Badge variant="secondary">25 pts</Badge>
          </div>
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <span>Achieve career milestone</span>
            <Badge variant="secondary">300 pts</Badge>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
