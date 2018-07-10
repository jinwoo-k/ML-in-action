package ch12_fp_growth

object FpGrowth {
  type Occurs = Int
  type HeaderTable[A] = Map[A, (Occurs, Option[Node[A]])]

  def main(args: Array[String]): Unit = {
    val dataSet = List(
      List('r', 'z', 'h', 'j', 'p'),
      List('z', 'y', 'x', 'w', 'v', 'u', 't', 's'),
      List('z'),
      List('r', 'x', 'n', 'o', 's'),
      List('y', 'r', 'x', 'z', 'q', 't', 'p'),
      List('y', 'z', 'x', 'e', 'q', 's', 't', 'm'))



  }

  def createHeaderTable[A](dataSet: List[List[A]], minSupport: Int = 1): HeaderTable[A] =
    dataSet.flatten.flatten.groupBy(identity)
      .mapValues(l => (l.size, None))
      .filter { case (a, (occur, nodeOpt)) => minSupport < occur }
      .withDefaultValue((0, None))

  def createTree[A](dataSet: List[List[A]]): Node[A] = {
    val headerTable = createHeaderTable(dataSet)

    def makeTree(prevNode: Node[A], transaction: List[A]): Node[A] = {
      val sortedTransaction = transaction.map(a => (a, headerTable(a)))
        .filter { case (_, (occurs, _)) => 0 < occurs }
        .sortBy { case (_, (occurs, _)) => -occurs }


    }

  }

  def update[A](items: List[A], node: Node[A], headerTable: HeaderTable[A]): (Node[A], HeaderTable[A]) = items match {
    case h :: t => {
      val child = if (node.children.contains(h)) {
        node.children(h).inc()
      } else {
        val c = new Node(h, 1, None, Some(node), Map.empty)
        node.updateChild(c)
      }
      update(t, child)
    }
    case _ => (node, headerTable)

  }
}

case class Node[A](name: A, count: Int, nodeLink: Option[Node[A]], parent: Option[Node[A]], children: Map[A, Node[A]]) {
  def inc(cnt: Int = 1): Node[A] = {
    val newNode = this.copy(count = this.count + cnt)
    parent.get.updateChild(newNode)
    newNode
  }

  def updateChild(child: Node[A]): Node[A] = {
    val newNode = this.copy(children = children.updated(child.name, child))
    parent.foreach(_.updateChild(newNode))
    newNode
  }


}

