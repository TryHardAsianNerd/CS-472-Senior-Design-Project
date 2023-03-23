using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Tilemaps;

public class PathFinding
{
    private Tilemap tileMap;
    private int _width, _height;

    public PathFinding(Tilemap tileMap)
    {
        this.tileMap = tileMap;
        _width = tileMap.size.x / 2;
        _height = tileMap.size.y / 2;
    }

    public List<Vector3> getPath(Vector3Int current, Vector3Int target)
    {
        BaseTile currentNode = (BaseTile)tileMap.GetTile(current);
        currentNode.distance = 0;

        while (true) {
            checkAdjacentNodes(currentNode);
            BaseTile nextNode = getNextNode();

            if(nextNode == null) {
                List<Vector3> path = new List<Vector3>();

                // Get target node
                nextNode = (BaseTile)tileMap.GetTile(new Vector3Int(target.x, target.y, 0));

                // Get path
                while(nextNode.parent != null) {
                    path.Add(new Vector3(nextNode.x, nextNode.y, 0));
                    nextNode = nextNode.parent;
		        }

                resetGrid();
                return path;
	        }
            currentNode = nextNode;
	    }
    }

    private void resetGrid()
    {
        for(int x=-1*_width; x<_width; x++) {
            for(int y=-1*_height; y<_height; y++) {
                BaseTile tile = (BaseTile)tileMap.GetTile(new Vector3Int(x, y, 0));
                tile.visited = false;
                tile.distance = -1;
                tile.parent = null;
                tile = null;
	        }
	    }
    }

    private BaseTile getNextNode()
    {
        BaseTile nextNode = null;
        for(int x=-1*_width; x<_width; x++) {
            for(int y=-1*_height; y<_height; y++) {
                BaseTile tile = (BaseTile)tileMap.GetTile(new Vector3Int(x, y, 0));

                if(!tile.Collision() && !tile.visited && tile.distance > 0) {
                    if (nextNode == null) nextNode = tile;
                    else if (tile.distance < nextNode.distance) nextNode = tile;
		        }
                tile = null;
	        }
	    }
        return nextNode;
    }

    public void checkAdjacentNodes(BaseTile currentNode)
    {
        for(int y=-1; y<=1; y++) { 
            for(int x=-1; x<=1; x++) {
                if (y == 0 && x == 0) continue; // Skip center node
                if(currentNode.x + x >= -1*_width && currentNode.x + x < _width &&
		           currentNode.y + y >= -1*_height && currentNode.y + y < _height) {

                    BaseTile adjacentTile = (BaseTile)tileMap.GetTile(new Vector3Int(currentNode.x + x, currentNode.y + y, 0));

                    float xdistance = currentNode.x - currentNode.x + x;
                    float ydistance = currentNode.y - currentNode.y + y;
                    int distance = (int)(Mathf.Sqrt(Mathf.Pow(xdistance, 2) + Mathf.Pow(ydistance, 2)) * 10);

                    if(currentNode.distance + distance < adjacentTile.distance ||
			           adjacentTile.distance == -1) {
                        adjacentTile.distance = currentNode.distance + distance;
                        adjacentTile.parent = currentNode;
		            }
                    adjacentTile = null;
		        }
	        }
	    }
        currentNode.visited = true;
    }
}
